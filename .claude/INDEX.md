# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11397  GET              /                                                dashboard
 12915  GET              /api/abo/status                                  api_abo_status
 12896  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 12014  GET              /api/automation/status                           api_automation_status
 12036  POST             /api/automation/toggle                           api_automation_toggle
 21538  GET              /api/channel/categories                          api_channel_categories
 21544  POST             /api/channel/set                                 api_channel_set
 21395  GET              /api/channels/status                             api_channels_status
 21097  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21080  GET              /api/clips                                       api_clips
 21126  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21026  GET              /api/debug/threads                               api_debug_threads
 12901  GET              /api/events                                      api_events
 12392  GET              /api/events/stream                               api_events_stream
 12251  GET              /api/health                                      api_health
 21057  POST             /api/highlights/config                           api_highlights_config
 11327  POST             /api/login                                       dashboard_login_submit
 13133  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12321  GET              /api/notify/status                               api_notify_status
 12332  POST             /api/notify/test                                 api_notify_test
 12969  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12946  GET              /api/proxy/trend                                 api_proxy_trend
 21144  GET              /api/tts/<fn>                                    api_tts_file
 21921  GET              /api/upload_window                               api_upload_window
 12494  GET              /archive/<int:eid>/download                      archive_download
 12520  GET              /download/<int:recording_id>                     download
 12453  GET              /health                                          health
 20898  GET              /healthz                                         healthz
 11318  GET              /login                                           dashboard_login_page
 11352  GET              /logout                                          dashboard_logout
 11359  GET              /manifest.webmanifest                            pwa_manifest
 21902  GET              /overlay                                         overlay_page
 11383  GET              /pwa-icon-<variant>.png                          pwa_icon
 11369  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (357)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1074  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   776  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   941  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   921  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   959  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   879  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   387  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   398  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   408  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   431  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   438  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   449  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   582  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   680  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1315  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1347  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   372  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
  1027  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
  1003  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1180  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1228  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1282  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1138  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   978  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   548  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   827  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   694  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   677  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   669  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   482  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   498  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   871  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   400  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   431  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   836  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   856  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   728  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    86  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   417  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   408  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    39  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    51  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   556  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   528  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   253  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   188  POST             /api/cookies/bereinigen                          api_cookies_bereinigen   [nc/routes/settings.py]
   133  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    74  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    81  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   496  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   274  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   301  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   399  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   338  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   356  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   261  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    86  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   132  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   146  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   161  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   193  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   178  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    89  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   111  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   132  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   149  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    79  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   208  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    43  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   229  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   249  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   276  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   161  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    44  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   151  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   126  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   182  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    77  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
   100  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   216  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   847  GET              /api/ki/wahl                                     api_ki_wahl   [nc/routes/ai.py]
   856  POST             /api/ki/wahl                                     api_ki_wahl_setzen   [nc/routes/ai.py]
   225  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   247  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   174  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   131  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   181  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   173  GET              /api/leitstand                                   api_leitstand   [nc/routes/leitstand.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    79  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   111  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   121  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    53  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    71  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   146  GET              /api/mcp/export                                  api_mcp_export   [nc/routes/mcp.py]
    85  GET              /api/mcp/server                                  api_mcp_server_liste   [nc/routes/mcp.py]
   111  POST             /api/mcp/server                                  api_mcp_server_anlegen   [nc/routes/mcp.py]
   116  POST             /api/mcp/server/<sid>                            api_mcp_server_aendern   [nc/routes/mcp.py]
   121  DELETE           /api/mcp/server/<sid>                            api_mcp_server_loeschen   [nc/routes/mcp.py]
   132  POST             /api/mcp/server/<sid>/test                       api_mcp_server_test   [nc/routes/mcp.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   101  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    67  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    78  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   148  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   143  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   134  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    54  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    93  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   326  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   293  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   171  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   992  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1133  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1161  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1181  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   979  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1041  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1028  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
  1009  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   647  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   642  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   690  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   573  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   907  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   664  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   627  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   600  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   881  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   744  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   840  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   739  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   672  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   463  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   924  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   551  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   802  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   957  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   942  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   507  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   734  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   720  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   703  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   760  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1324  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1478  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1288  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   860  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   749  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   509  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   487  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   553  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   570  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   622  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   459  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   274  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   167  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   644  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   422  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   136  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   583  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   609  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   200  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   225  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   397  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   614  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   604  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   644  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   239  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   460  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   489  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   409  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   422  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   518  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   395  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   270  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   315  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   339  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   326  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   166  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   284  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   376  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   431  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
   133  GET              /overlay/chat                                    overlay_chatbild   [nc/routes/overlay.py]
   148  GET              /overlay/chat.json                               overlay_chatbild_daten   [nc/routes/overlay.py]
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2728  /about                  Ueber diesen Bot
  1269  /ai                     
  2728  /aireset                KI-Kontext zuruecksetzen
  1714  /ask                    
  1370  /assign_role            
  1428  /ban                    
  2684  /botstats               
  2728  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2728  /bulkadd                Mehrere User auf einmal tracken · a b c
  2728  /cleanup                Alte Aufnahmen aufraeumen
  1987  /clearwarns             
  2648  /clip                   
  2633  /clipoftheweek          
  1850  /clips                  
  2728  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1325  /create_category        
  1296  /create_channel         
  1360  /create_group           
  1335  /create_role            
  1311  /create_voice           
  1591  /daily                  
  2728  /diag                   Vollstaendige Diagnose
  2728  /einnahmen              Einnahmen und Spenden
  1743  /event                  
  1785  /events                 
  1890  /follow                 
  1879  /help                   
  1416  /kick                   
  1563  /leaderboard            
  2728  /live                   Live-Status sofort pruefen · @user
  1837  /livenow                
  2728  /logs                   Letzte Fehler aus dem Log
  2728  /pause                  Tracking pausieren · @user
  1865  /post_test              
  1675  /profile                
  1454  /purge                  
  2728  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2728  /quota                  Speicher-Quota
  1550  /rank                   
  1825  /recstatus              
  1382  /remove_role            
  2728  /report                 Azrael-Sentinel-Wochenreport
  1282  /restream_status        
  2728  /resume                 Tracking fortsetzen · @user
  1394  /set_channel_perms      
  1514  /setup_community        
  1531  /setup_targets          
  1811  /spenden                
  1924  /stats                  
  1241  /status                 
  2728  /stoprec                Laufende Aufnahme sauber beenden · @user
  2025  /streaminfo             
  2728  /summary                Tageszusammenfassung
  2728  /sysres                 System-Ressourcen
  2728  /teststream             Recorder-Selbsttest · @user
  2728  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1440  /timeout                
  1997  /topstreamers           
  2728  /topusers               Top-Streamer nach Aufnahmen
  1150  /track                  
  2728  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
  1254  /tracklist              
  1906  /unfollow               
  2728  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
  1203  /untrack                
  1945  /warn                   
  1973  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2832  on_member_join
  2789  on_message
  2749  on_raw_reaction_add
  2869  on_ready
```

## Top-Level-Symbole in telegramversand.py (10 Funktionen)

```
   456-460    _fehler_meldung
   557-585    _nachteilen
   588-618    _neu_kodiert
   463-526    _teile_bereiten
   416-433    _teile_freigeben
   401-413    _teile_holen
   529-554    _teilen_oder_reparieren
    59-74     konfiguriere
    77-384    split_and_send_video
   436-453    teil_pause_s
```

## Top-Level-Symbole in discordbot.py (70 Funktionen)

```
  2132-2183   _award_xp
  1468-1484   _bereiche_bericht
   557-568    _clip_kopieren
  2348-2377   _clip_week_leader
  2401-2412   _clipoftheweek_loop
   668-721    _clips_einsortieren
  2988-3052   _community_events_loop
   359-368    _dc_abbruch_melden
  2102-2108   _dc_bereit
  2059-2081   _dc_client
   342-356    _dc_fehlerart
  2084-2093   _dc_offen
  2111-2123   _dc_warten
  3092-3127   _disc_automod_check
   475-480    _disc_sprache_setzen
  2186-2234   _discord_ai_automod
   893-935    _discord_automod
  2237-2257   _discord_azrael_reply
  2552-2945   _discord_run_once
   249-326    _discord_start
   371-425    _ensure_discord_invite
  2951-2985   _ensure_error_channel
   504-517    _ensure_rank_roles
  1113-1127   _ensure_team_roles
  3055-3085   _error_channel_loop
   952-966    _follow_erlaubt
   611-615    _getrackte_nutzer
   945-949    _guard
   826-890    _handle_voice_ai
   483-501    _is_admin
   583-608    _link_video
  2302-2310   _liveboard_loop
   969-971    _name_ungueltig
  1007-1041   _on_level_up
   749-750    _par_chat_id
  2380-2398   _post_clip_of_week
  2313-2331   _post_weekly_digest
   520-546    _provision_base_channels
   984-1004   _rang_pruefen
   974-981    _rang_satz
  1817-1913   _reg_betrieb
  1487-1580   _reg_community_setup
  1583-1664   _reg_daily_profil
  1707-1804   _reg_frage_events
  1228-1284   _reg_info
  1408-1465   _reg_moderation
  1667-1704   _reg_profil
  1351-1405   _reg_rollen
  1287-1348   _reg_server
  1807-1814   _reg_spenden
  1916-2008   _reg_streamer
  2011-2056   _reg_system
  1141-1225   _reg_tracking
  1076-1110   _run_tg_handler
   812-823    _shim_chat_id
  2510-2539   _stern_an_telegram
  2542-2549   _stern_anspruch_zurueck
  2415-2507   _stern_highlight
   166-228    _uebernehmen
   571-580    _umzugsmarken
  2266-2299   _update_liveboard
   798-809    _voice_dauer
   769-776    _voice_max_s
   779-795    _voice_zulassen
  2334-2345   _weekly_digest_loop
   549-554    _ziel_guild
   618-665    _ziele_abgleichen
   730-746    _ziele_sync_loop
   724-727    _ziele_takt_min
   231-234    starte
```

## Top-Level-Symbole in bot.py (594 Funktionen, 4 Klassen)

```
 26822-26844  _abbruch_datenbank_unlesbar
  2909-2910   _abo_key
  2930-2948   _abo_probe_dump
 26944-26960  _abschied_wachen
 26963-26981  _abschluss
 17086-17093  _ad_allowlist
 18252-18258  _agent_for
 18261-18277  _ai_telemetry
 18793-18811  _alert
 22342-22392  _alert_monitor_loop
 19498-19555  _alte_beilagen_einsammeln
 22779-22841  _announce_loop
  3860-3870   _anthropic_key
  3873-3875   _anthropic_model
 10850-10853  _arg_int
  2901-2906   _as_dict
 26508-26517  _async_exc_handler
 18982-19004  _audio_tap_cmd
 20046-20105  _audio_tap_melden
 19018-19042  _audio_tap_sammler
 23104-23143  _aufnahme_an_server
 10198-10235  _aufnahme_beim_stopp_sichern
 19440-19461  _aufnahme_chat_ausklang
 19424-19437  _aufnahme_chat_beginnen
 19583-19604  _aufnahme_chat_dienst
 19793-19859  _aufnahme_chat_einarbeiten
 19419-19421  _aufnahme_chat_modus
 19607-19656  _aufnahme_chat_nachtrag
 19464-19495  _aufnahme_chat_vormerken
 19574-19580  _aufnahme_chat_wecken
 25624-25626  _aufnahme_deckel
 19659-19680  _aufnahme_fertigmachen
 23025-23087  _aufnahme_nach_discord
 10238-10256  _aufnahme_platz_frei
 10123-10168  _aufnahme_verteilen
 26908-26928  _aufnahmen_abschliessen
 26847-26905  _aufraeumen
 11139-11208  _auth_cookie
 11093-11135  _auth_guard
  2129-2134   _auto_on
 20761-20787  _auto_restream_loop
 14400-14442  _avatar_frames_laden
 17136-17149  _azrael_brain_kontext
 24056-24071  _azrael_broadcast_reply
 23956-23978  _azrael_chat_reply
 23928-23953  _azrael_chat_should_reply
 23984-23986  _azrael_gate_cfg
  4404-4419   _azrael_ki
 18280-18294  _azrael_live_state
  4422-4445   _azrael_lokal
 21788-21802  _azrael_overlay_state
 18336-18344  _azrael_persona_kern
 18675-18729  _azrael_proactive_loop
 18100-18156  _azrael_reaction_to_chats
 23989-23996  _azrael_reply_all_chats
  4448-4463   _azrael_schweigt_melden
 23915-23925  _azrael_self_names
 24024-24053  _azrael_send_to
 14361-14397  _azrael_spricht
 14719-14732  _azrael_stimme_stumm
 18300-18333  _azrael_system
 22476-22479  _backup_active
 22557-22570  _backup_loop
  5662-5685   _betreiber_pruefen
 25713-25717  _betrieb
 26581-26590  _brain_crowdsec_snap
 26749-26752  _brain_db_health
 24915-24955  _brain_fragen
 22263-22272  _brain_growth_loop
 11526-11553  _brain_growth_snapshot
  2820-2854   _brain_hint_delay
 26653-26688  _brain_moderation_snap
  6982-7010   _brain_notify
 26755-26777  _brain_recording_snap
 26593-26650  _brain_restream_health
 26780-26793  _brain_tiktok_status_snap
 12367-12388  _browser_push
 14766-14770  _build_restream_cmd
  5688-5715   _can_stop_tracking
  2240-2262   _capture_set_cookies
 12999-13002  _cfg_get
 13005-13007  _cfg_set
 21499-21534  _channel_set_all
 13442-13445  _chat_connected
 13448-13464  _chat_disconnected
 19568-19571  _chat_einarbeiten_async
  9614-9644   _chat_is_forum
 19388-19413  _chat_listener_abbauen
  9786-9821   _chat_migriert
  9824-9825   _chat_migriert_async
 13478-13480  _chat_sanitize
 13427-13439  _chat_stat
  4278-4290   _check_ai_models_sync
 11721-11764  _classify_pool_anonymity
   920-942    _claude_chat_sync_metered
 10895-10901  _client_ip
 23557-23571  _clip_chat_ass
 22925-22968  _clip_prune
 22971-22981  _clip_recfile_for
 23471-23545  _clip_schneiden
 23574-23580  _clip_should_velocity
 23146-23232  _clip_to_discord
 19754-19759  _clips_abwarten
  4060-4069   _close_ai_session
 24102-24117  _cohost_broadcast
 24087-24088  _cohost_cfg
 24143-24155  _cohost_fire_highlight
 24091-24099  _cohost_gate
 24120-24140  _cohost_highlight
  7312-7373   _cookie_alarm_loop
  2330-2331   _cookie_autofetch_info
  2314-2318   _cookie_autorefresh_info
 26178-26200  _cookie_bezug_loop
 26203-26228  _cookie_bezug_runde
  2217-2221   _cookie_header
 10904-10909  _cookie_sicher
  2343-2357   _cookies_selbst_holen
  4553-4555   _create_index_safe
  7198-7225   _daily_summary_loop
  3386-3411   _darf_ytdlp_nachschlagen
 12535-12556  _dashboard_adresse
 10924-10928  _dashboard_hostnamen
  1540-1570   _dashboard_trackings_umziehen
 23548-23554  _datei_weg
 22316-22339  _db_maintenance_loop
  7148-7195   _db_vacuum_loop
 12559-12568  _deck_intern_url
 17109-17133  _detect_foreign_ad
  1810-1821   _diag_path_owner
 18580-18625  _director_finalize
 20036-20043  _director_for
 18529-18577  _director_mark
 23384-23387  _disc_state_get
 23390-23397  _disc_state_set
 23090-23101  _discord_aufnahme_gilden
 22244-22253  _discord_bot_starten
 22207-22218  _discord_einladung_merken
 22256-22260  _discord_invite
 22221-22241  _discord_kontext
 23345-23381  _discord_live_thread
 18732-18744  _discord_notify
 22179-22204  _discord_ops_alert
 23243-23341  _discord_post_user
 22844-22850  _discord_stop
  7228-7309   _disk_alarm_loop
 26049-26100  _disk_autoclean
 26364-26377  _disk_guard_loop
 14340-14347  _drossel_hoeher
 14336-14337  _drossel_stufe
 14350-14358  _drossel_zuruecksetzen
 12737-12739  _dump_all_threads
 25720-25734  _einstellungen_startzeile
  2389-2470   _ensure_cookie_file_netscape
  9715-9718   _ensure_notify_topic
 11871-11908  _ensure_proxy_ready
  9654-9677   _ensure_topic
   763-765    _env_int
   768-770    _env_int_range
 18777-18790  _event_webhook
 13225-13238  _evolution_loop
  6388-6422   _extract_file_payload
  1522-1537   _fanout_ziele
 26984-27049  _fatal_vom_botteil
 25629-25644  _fd_grenze_anheben
  5230-5240   _fehler_text
 11620-11638  _fetch_proxy_list
 19357-19385  _fetch_tiktok_room_id
   848-851    _ff_cmd
 19767-19790  _ffprobe_masse
 14264-14280  _fifo_schreiber_wecken
 14052-14057  _find_chromium
  3781-3783   _find_external_recorder
  2533-2535   _find_stream_urls
 13048-13073  _fire_webhooks
  8261-8271   _fork_safe
   953-966    _freeai_chat_sync_metered
  4048-4057   _get_ai_session
  8089-8129   _get_live_info
  3230-3237   _get_resolve_semaphore
  8786-9221   _handle_single_tracking
 25833-25835  _hb
 25838-25855  _hb_while
 21011-21022  _healthz_fuer_aufrufer
 25879-25907  _heap_zurueckgeben
 11212-11229  _herkunft_guard
 13492-13494  _highlight_cfg
 13497-13526  _highlight_observe
 12571-12581  _htmlov_basis_url
 14124-14132  _htmlov_bild_schreiben
 14093-14121  _htmlov_dauerbrowser
 14072-14090  _htmlov_screenshot_cmd
 14060-14069  _htmlov_url
 19044-19054  _httpx_proxy
 13081-13093  _in_quiet_hours
 26808-26819  _init_db_oder_abbruch
 27663-27694  _install_fast_eventloop
 10745-10799  _install_fast_json
 12742-12758  _install_faulthandler
 20807-20816  _intel_ensure_schema
 20859-20894  _intel_index_loop
 20828-20843  _intel_index_one
 20819-20825  _intel_semantic
  5640-5660   _is_authorized
  8612-8633   _is_dead
  2029-2036   _is_process_running
  7012-7019   _is_quiet_hours
  1411-1420   _is_upload_window
  5062-5077   _iso
 10912-10921  _ist_lokal
 10834-10847  _json_error_handler
  4122-4141   _ki_nach_deckwahl
  4199-4208   _ki_rueckfall_melden
  8487-8494   _kick_cluster_gefunden
  8422-8484   _kick_cluster_weiter
  7061-7103   _kick_follower_count
  7045-7048   _kick_slug
  8392-8419   _kick_ws_pause
 26796-26805  _kickmod_boot
 26144-26147  _lagebild_discord_aufnahme
 26157-26161  _lagebild_kick_chat
 26150-26154  _lagebild_overlay
 26164-26166  _lagebild_spendenziel
 26131-26141  _lagebild_upload
 13110-13112  _latest_popularity
  1966-1975   _laufstand
 26319-26361  _laufstand_loop
 25757-25795  _leistung_erheben
  7978-8005   _link_video_senden
  8773-8784   _live_check_frist_melden
  2964-2977   _live_ohne_stream
 20444-20493  _live_react_loop
 20108-20430  _live_react_worker
  3629-3743   _live_status_aufloesen
 18159-18170  _live_transcript_push
 20432-20442  _live_users
 18628-18672  _living_title_loop
 22482-22554  _local_backup_scan
  4996-5025   _lock_update
 10816-10830  _log_5xx
 25798-25830  _log_schleuse_pruefen
   838-845    _log_sicher
 14778-14790  _looks_like_codec_err
 14773-14775  _looks_like_source_expired
  8310-8340   _loop_fehler
 12761-12770  _loop_heartbeat
 25535-25568  _loop_lag_monitor
 25582-25602  _loop_stockung_melden
 25605-25615  _loop_takt_starten
 12773-12846  _loop_watchdog_thread
 18036-18053  _loyalty_add
 18027-18033  _loyalty_get
 18056-18064  _loyalty_top
  5341-5360   _manual_status
  8635-8636   _mark_dead
 12091-12107  _marketing_loop
 24003-24021  _maybe_handle_command
 26463-26487  _maybe_hype_clip
 22894-22922  _meme_klassifizieren
 19683-19751  _meme_zusammenschnitt
  4540-4545   _migrate_columns
 24285-24296  _mod_is_exempt
 24299-24304  _mod_warn_first
 24307-24310  _mod_warn_text
 13267-13286  _modlog
 13250-13264  _modlog_schreiben
  1104-1106   _multistream_targets
  3414-3450   _nachschlag_ytdlp
  8274-8275   _nc_create_subprocess_exec
  8278-8279   _nc_create_subprocess_shell
 12205-12222  _news_loop
 13309-13311  _normalize_ingest
  2751-2768   _note_check_duration
  9709-9712   _notify_topic_name
  4144-4149   _nur_free
  4152-4156   _nur_free_sync
  4159-4196   _nur_lokal_sync
  2955-2961   _offline_ergebnis
  3453-3476   _ohne_url_melden
 18185-18193  _oracle_memories
 18480-18514  _oracle_memorize
 18196-18209  _oracle_persona
 18178-18182  _oracle_recent_text
 13715-13716  _ov_atomic_write
 13706-13708  _ov_bar
 17014-17026  _ov_clip_text
 13711-13712  _ov_oneline
 13805-13866  _overlay_kanalweit
 21837-21895  _overlay_push
 14006-14049  _overlay_render_size
 13869-13896  _overlay_sendebild_schreiben
 13378-13382  _overlay_session_reset
 21804-21806  _overlay_src_ok
 13725-13737  _overlay_takt
 17096-17106  _own_invites
 14001-14003  _parse_size
  7623-7656   _pause_resume_cmd
  2268-2312   _persist_refreshed_cookies
  2171-2203   _pick_checked_pull_proxy
 10978-10993  _pin_auth_value
 11082-11083  _pin_clear_fail
 11046-11049  _pin_global_gesperrt
 10999-11010  _pin_hmac_schluessel
 11052-11059  _pin_locked
 11062-11079  _pin_note_fail
 11013-11034  _pin_ok
 21632-21657  _piper_pick_model
 21717-21782  _piper_say
 13010-13045  _post_json_threaded
 13980-13998  _probe_video_size
  2057-2074   _proc_is_recorder
 11840-11868  _proxy_pool_refresh_loop
  2137-2168   _proxy_report_recording
  9360-9444   _pruef_runde
  9319-9357   _pruefstand_melden
 25664-25675  _pruefung_verworfen
 12727-12729  _prune_stall_dumps
  2334-2340   _pull_proxy_still
 18748-18774  _push_notify
 11276-11278  _pwa_dir
 11689-11706  _quick_validate_proxy
 13076-13078  _quiet_hours_config
 11241-11274  _rate_guard
  2980-3008   _raumsperre_fragen
 17997-18003  _react_warn
  8176-8215   _reap_proc
 10931-10947  _rebinding_melden
 10053-10120  _rec_auto_abschalten
 10000-10050  _rec_frueh_getrennt
  9865-9945   _rec_kategorie_melden
  9948-9997   _rec_totstreak_fortschreiben
  2791-2813   _record_check_outcome
   833-835    _redact_stream_urls
 11767-11837  _refresh_proxy_pool
  2568-2659   _resolve_via_html
  3011-3207   _resolve_via_webcast_api_v2
  3275-3362   _resolve_via_ytdlp
 23614-23743  _resolve_youtube_ingest
  2544-2565   _resolver_stumm
 13361-13372  _restream_active_sources
 14445-14583  _restream_avatar_feeder_start
 14586-14596  _restream_avatar_feeder_stop
 19862-20000  _restream_chat_guardian
 13529-13614  _restream_chat_push
 13691-13701  _restream_chat_push_async
 14283-14300  _restream_chatbild_start
 26691-26746  _restream_durchreicher
 14135-14261  _restream_html_overlay_start
 14303-14323  _restream_html_overlay_stop
 20745-20758  _restream_liste_abgleichen
 13320-13343  _restream_overlay_files
 20496-20528  _restream_platform_state
 20704-20739  _restream_resume_after_restart
 13645-13662  _restream_soll_schreiben
 13665-13688  _restream_status_schreiben
 14644-14716  _restream_tts_enqueue_wav
 13942-13974  _restream_tts_feeder
 13939-13940  _restream_tts_fifo_path
 14599-14626  _restream_tts_start
 14628-14642  _restream_tts_stop
 20534-20701  _restream_verify_loop
 22447-22459  _retention_loop
 22441-22444  _retention_scan
  2912-2914   _room_is_abo
  6425-6580   _run_ai_call
 12869-12882  _run_async_from_flask
 27652-27660  _run_selfcheck_and_exit
 22462-22473  _s3_client
  8662-8732   _safe_send
  5304-5320   _sample_net_throughput
 27632-27649  _sc_bericht
 27573-27629  _sc_dienste
 27480-27570  _sc_ki_und_stimme
 27431-27477  _sc_umgebung
  2857-2887   _schedule_next_check
 22395-22438  _scheduler_loop
  4548-4550   _schema_pk
 12885-12890  _scraper_session
 24313-24352  _screen_full
 12267-12304  _sec_headers
  2528-2530   _select_stream_from_data_section
 27341-27428  _selfcheck
  9721-9755   _send_live_notice
  1434-1438   _should_defer_upload
 22984-23022  _shrink_for_discord
 11281-11314  _sicheres_ziel
 22275-22313  _sicherheits_erinnerung_loop
 26384-26401  _sign_health_check
 26404-26423  _sign_health_loop
  5080-5110   _sitzung_bestimmen
 20994-21004  _sparen_lage
  8291-8302   _spawn
 28085-28115  _spawn_from_flask
 25678-25684  _speicher_maps
 25687-25702  _speicher_pflegen
 19056-19354  _start_chat_listener
 25647-25661  _start_gesperrt
 12849-12866  _start_loop_watchdog
 12153-12202  _stats_loop
 12132-12135  _stats_output_path
 12138-12150  _stats_write
 21669-21683  _stimme_saubern
 21690-21714  _stimme_schon_gesagt
  9300-9316   _storage_cleanup_loop
 26443-26450  _story_for
  3805-3811   _stream_url_expiry
  3813-3818   _stream_url_ttl
 17059-17066  _streamer_persona_get
 22579-22737  _system_backup
 22746-22776  _system_backup_loop
 12687-12705  _task_auf_bot_schleife
 25192-25208  _telegram_befehlsmenue
  8343-8389   _telegram_polling_fehler
 25224-25259  _telegram_starten
  1492-1519   _telegram_ziele
 11641-11680  _test_proxy
 12063-12079  _testpush_resolve_live
 19762-19764  _text_schreiben
  7945-7953   _tg_botname
  7903-7942   _tg_ki_dialog
  9773-9783   _tg_migriert_laden
  9769-9770   _tg_migriert_pfad
  8638-8659   _tg_sprache_setzen
  9583-9593   _tg_topics_load_into_mem
  9580-9581   _tg_topics_path
  9595-9602   _tg_topics_save
 10950-10960  _token_ok
  9680-9696   _topic_anlegen
  9605-9612   _topic_forget
 13096-13107  _tracking_max_duration
  4810-4824   _tracking_remove_cleanup
  4841-4853   _tracking_resume_cleanup
  1868-1891   _try_attach_file_handler
 21659-21667  _tts_cleanup
 26103-26123  _tunnel_lage
 26264-26316  _tunnel_wacht_loop
 21162-21215  _twitch_channel_status
 24355-24503  _twitch_chat_loop
 23403-23416  _twitch_clip_versuchen
 24166-24272  _twitch_eventsub_loop
  1623-1643   _upload_queue_abarbeiten
  1470-1490   _upload_queue_add
  1588-1596   _upload_queue_count
  1646-1689   _upload_queue_eintrag
  1440-1444   _upload_queue_load
  1692-1718   _upload_queue_nachher
  1430-1432   _upload_queue_path
  1573-1577   _upload_queue_remove
  1464-1468   _upload_queue_save
  1447-1462   _upload_queue_schreibbar
  1580-1586   _upload_queue_update
 10171-10195  _upload_rest_sichern
  1598-1620   _upload_window_loop
  8149-8156   _uptime_s
 13297-13306  _url_host
  3479-3577   _url_nachschlag
   913-917    _usage_record_claude
 26556-26578  _v37_pause_source
 26520-26530  _v37_restream_restart
 26533-26553  _v37_unpause_source
  8561-8605   _verbindung_verloren
  7106-7137   _viewer_sample_loop
 11086-11089  _wants_html
  8159-8173   _warn_empty_env
 25910-26035  _watchdog_loop
 23887-23895  _wchat_thank_ok
 26231-26261  _werkzeug_wacht_loop
 18816-18854  _whisper_get_model
  8250-8258   _whisper_native_section
 17984-17990  _whisper_pool
 18948-18980  _whisper_segments
 18856-18872  _whisper_stumm
 18875-18945  _whisper_transcribe
 13778-13802  _write_restream_overlay
 13740-13775  _write_restream_overlay_async
 24527-24626  _youtube_api_chat_loop
 21218-21321  _youtube_api_status
 21324-21391  _youtube_channel_status
 24629-24795  _youtube_chat_loop
 23419-23444  _youtube_clip_versuchen
 23749-23762  _youtube_restream_autoconfig
 23765-23789  _youtube_restream_autoconfig_inner
 23856-23884  _youtube_send
 21455-21496  _youtube_set_channel
 23792-23826  _yt_access_token
 23829-23844  _yt_live_chat_id
 23852-23853  _yt_sendrate_cfg
 24506-24521  _yt_timeout
  3254-3255   _ytdlp_detect_available
  3270-3272   _ytdlp_einzeln
  3257-3268   _ytdlp_note_result
 12732-12734  _zombie_child_count
 25737-25754  _zustand_kennzahlen
  8025-8049   about
  4729-4733   add_ai_log_entry
  5118-5212   add_recording
  4785-4802   add_tracking
  6583-6616   ai
  4299-4396   ai_chat
  4495-4505   ai_history_append
  4507-4512   ai_history_clear
  4484-4493   ai_history_load
  4469-4482   ai_rate_limit_check
  6645-6653   aireset
 18347-18366  azrael_chat
 24800-24903  brain_cmd
  3821-3826   build_recording_cmd
  4805-4808   bulk_add_trackings
  7376-7435   bulkadd
  9447-9563   check_all_trackings
  4856-4868   claim_live_transition
 17152-17916  class KickModerator
 14793-16902  class RestreamManager
  5028-5029   class _AufnahmeLockVerloren
  8497-8558   class _KickClusterSuche
 11951-11993  classify_proxy_anonymity
  6691-6888   cleanup
  5581-5587   cleanup_old_recordings
  5053-5060   clear_recording
 23447-23468  clip_moment
  7498-7574   cookies_cmd
  7577-7620   cookies_datei_cmd
  4776-4782   count_trackings_for_chat
  4716-4727   decide_preferred_recorder
  6083-6230   diag
 25074-25135  einnahmen_cmd
  4677-4693   finish_recording_attempt
  4829-4831   get_all_active_trackings
  5214-5217   get_all_recordings
  4655-4658   get_archive_entry
  2374-2379   get_cookie_health
  5284-5290   get_event_log
  4700-4714   get_last_recording_attempt
  3580-3622   get_live_status
  5295-5298   get_priority_poll_interval
  4695-4698   get_recent_recording_attempts
  5219-5222   get_recording_by_id
  3988-4017   get_redis
  5575-5579   get_storage_stats
  5334-5336   get_tiktok_status_distribution
  4870-4879   get_tracking_state
  4826-4827   get_trackings_for_group
 10259-10727  handle_recording_finished
 25184-25189  hilfe_cmd
  4563-4628   init_db
  5857-5895   live
  8735-8765   live_check_worker
  4072-4119   llm_chat
  4229-4270   llm_chat_sync
  4214-4226   llm_list_models
  5243-5276   log_event
  1991-2024   log_recording_failure
  7770-7819   logs_cmd
 27052-27331  main
  6619-6642   on_ai_media
  7896-7900   on_ai_reply
  8008-8022   on_azrael_mention
  8054-8084   on_callback
  9828-9846   on_chat_migration
  7962-7975   on_link_video
 18372-18477  oracle_handle
  7659-7662   pause_tracking
  5630-5635   profile_keyboard
  5810-5854   quelle
  7721-7767   quota
  9223-9297   reaper_loop
  5330-5332   record_tiktok_status
  6658-6688   recstatus
  4019-4027   redis_get_json
  4030-4036   redis_set_json
 25211-25221  report_cmd
 11996-11998  report_proxy_result
  2662-2704   resolve_tiktok_live_stream
  7665-7668   resume_tracking
 25262-25515  run_bot
 12584-12678  run_flask
  4736-4742   save_tiktok_check
  5032-5051   set_recording_file
  4834-4838   set_tracking_paused
 25169-25181  spenden_cmd
  9852-9863   split_and_send_video
  5720-5762   start
  4661-4675   start_recording_attempt
  6891-6929   stats
  5499-5552   stop_manual_recording
  7671-7718   stoprec
  7030-7038   summary_cmd
  7822-7893   sysres
  6232-6376   teststream
  5764-5805   tiktok
  7438-7495   topusers
  5932-5989   track
  5897-5929   track_exact
  6014-6081   tracklist
  5363-5497   trigger_manual_recording
  4958-4993   try_acquire_recording_lock
 25138-25166  unpause_cmd
  5991-6012   untrack
 24958-25071  update_cmd
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
abwehrlage.py          auswerten, configure, crowdsec_status, crowdsec_via_lapi, cscli_bin, cscli_path, darf_journal_lesen, ssh_angriffe, sudo_hinweis
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, andere_kopien, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, dublette_loeschen, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, hat_quelle, run_archive_file_check, uebernehmen, unter_wurzel
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            aus_bestand, config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_cmd, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, kopf_cmd, kopf_masse, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, ist_zieldatei, join_reste, luecken, probe_cmd, sekunden, sitzung_id, teildatei, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelkontext.py       ausfall, block, fakten, letzte_erinnerung, nachricht, restream_quellen, sicher, streamer_waehlen
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_zugang, sys_backup, sys_hour, sys_keep
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            aendern, class FalscheForm, get, lesen, set_, upsert
channels.py            chat_anhaengen, chat_ausduennen, chat_eintraege, configure_chat, gehoert_in_kasten, letzte_zeit, quelle_aktiv, restream_active, yt_sendrate_cfg
chatbild.py            an, beenden, lage, starten
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, host_ist_lokal, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, bereinigen, class DateiGeaendert, class KeinDesktop, configure, desktop_pruefen, hole_gastcookies, schreibe, uebernehmen, zusammenfuehren
cookies.py             abgelaufen, auswahl, configure, gesundheit, hat_login, kritisch, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, pruefen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, mariadb_lage, set_pool, treiber_fehler, treiber_wunsch, vorrat_groesse, vorrat_lage, vorrat_leeren
dcspar.py              anzeige, client_optionen, puffer
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordaufnahme.py     abhilfe, an, an_alle, beschriftung, hochladen, teilen
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb, track_grenze_je_mitglied
discordrang.py         admin_rolle, admin_rolle_traegt, ist_eigentuemer, kanal_einwand, macht_rechte, rang_einwand, rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        bereich_kanal_holen, bereich_name, bereiche_an, class KeinPlatz, clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, einsortieren, gilde_waehlen, kanal_name, loeschbar, plan, platz, umzugsmarke, umzugsmarke_lesen, ziel_kanal
donations.py           configure, fmt_eur, kurse_aus_env, parse_number, summe_eur, to_eur, unknown_count, zeile_eur
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       bekannt, class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
encodeschlange.py      lage, last_frei, parallel, platz, platz_sync
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, schnappschuesse, schnappschuesse_kappen, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_kasten, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
forkriegel.py          class Vortritt
freeai.py              abhilfe, alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            anreichern, get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
heapzaum.py            arenen_wunsch, deckeln, lage, rss_mb, takt_min, zurueckgeben
herkunft.py            entscheiden
highlights.py          chat_raten, check, new_state, observe, score, zustand
httpsitzung.py         schliessen, sitzung, teilen
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, state_gueltig, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              azrael_lage, azrael_wahl, backend, beschriftung, brain_kette, deck_lage, deck_setzen, deck_wahl, etikett, gesamtzeit, herkunft, herkunft_loeschen, herkunft_setzen, herkunft_von, llm_zeiten, lokal_installiert, lokal_stand, lokal_zuerst, lokales_modell, normal, provider, vorrang, wartezeit, weg_zaehlen, zeitlimit
lagebild.py            bauen, dienst_quelle, dienste, dienste_lesen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
leitstand.py           bauen, drohnen, ereignis, ereignisse, kette, tafeln
linkvideo.py           abklingzeit_s, an, aufraeumen, ausgabe_lesen, befehl, bildunterschrift, configure, darf, grund, holen, ist_tiktok, links, max_dauer_s, sperre, werkzeug
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, schluessel, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
livemeldung.py         live_an, live_aus
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
mcpdienste.py          class Abgelehnt, class BestandUnbekannt, class Unbekannt, export, lage, liste, llama_adresse, loeschen, speichern, testen, webui
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, sql_bedingung, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, aktive_agenten, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
oeffentlichestats.py   configure, public_stats
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler, class SeiteNichtErreichbar, fifo_schreiben, lage, png_vollstaendig, teilen
overlaytext.py         alert_fuer, configure, follow_zeile, gehoert_zu, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok, overlay_url, quelle_zeile, reaktion_fuer, ziele
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
piperarbeiter.py       main
piperdienst.py         an, beenden, lage, sprechen
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, runde_gelaufen, uebersicht, vergessen
pruefschlange.py       erledigt, mit_frist, vorgemerkt, vormerken, zuruecksetzen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
raumkennung.py         grund, gueltig
raumsperre.py          deuten, faellig, lage, merken, snapshot, text, vergessen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      abhilfe, class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, chat_kasten, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamliste.py       abgleichen, an, ausschliessen, zulassen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in, tiktok_geschenk
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
schriftzeichen.py      emoji_hinweis, emoji_pakete_fehlen, schrift_von, tabelle, vermutlich_unzeichenbar, vorbereiten, zeichenbar
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        ausnahme_text, class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, class DumpFehler, dump_vollstaendig, mysqldump, pruefen, schwaerzen
sitzungsschluessel.py  laden, pin_schluessel
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
spendeninfo.py         krypto, paypal, paypal_url, stand, text
spendenziel.py         eingang, fenster_start, ist_monatlich, stand, summe, zeitraum, ziel_eur
sqldialekt.py          bei_konflikt
sqlguard.py            abbruch_nach, check_readonly, frist_ueberschritten, frist_unbekannt, mariadb_mit_frist, normalize, with_limit
sqlutil.py             zeitfenster_literal
stats.py               aufnahmen_je_tag, configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache, trefferquote
storage.py             class BestandUnbekannt, cleanup, forecast, notfall_raeumen, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
tagesbericht.py        bauen, configure
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, start_endgueltig, start_pause, starten, text, zuruecksetzen
textmore.py            configure_banned_cap, pre_nachrichten, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgantwort.py           angesprochen, echte_antwort, entscheiden, frage_ohne_namen, gemerkt, ist_brain_antwort, ist_ki_antwort, merken, ohne_brain_kopf, ohne_fuss
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, empfaenger, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
uploadschlange.py      angekommen, beiseite, class SchlangeUnlesbar, faellig, gleicher, lesen, nach_versuch, pause_s
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, dauer_aus_kopf, in_arbeit, ist_kaputter_container, ist_rest, kopier_teilen, messen, neu_kodieren, platz_reicht, reparieren, teile, teile_entfernen, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, eigene_url, intern_basis, ist_loopback, schema, threads, tls_lage, waehle
werkzeugpfad.py        alter_tage, befund, lage, nachahmen_aus, pruefen, voranstellen
whispercfg.py          bedarf_mb, benutzt, entladen_wenn_leer, frei_mb, gebrauch, geladen, leerlauf_s, name, rss_hinweis, verfuegbar, waehle, wechsel_pruefen
youtube_api.py         active_broadcast_params, ban_payload, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlparbeiter.py       main
ytdlpdienst.py         alle_beenden, anzahl, ausfuehren, laeufe_max, lage
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
zeitglaetter.py        ausdruck, bsf_args, filter_text, verfuegbar
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime, ohne_denkblock
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler, frische_intervalle
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
