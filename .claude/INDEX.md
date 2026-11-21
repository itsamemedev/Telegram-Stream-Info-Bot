# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11301  GET              /                                                dashboard
 12819  GET              /api/abo/status                                  api_abo_status
 12800  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11918  GET              /api/automation/status                           api_automation_status
 11940  POST             /api/automation/toggle                           api_automation_toggle
 21420  GET              /api/channel/categories                          api_channel_categories
 21426  POST             /api/channel/set                                 api_channel_set
 21277  GET              /api/channels/status                             api_channels_status
 20979  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20962  GET              /api/clips                                       api_clips
 21008  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20908  GET              /api/debug/threads                               api_debug_threads
 12805  GET              /api/events                                      api_events
 12296  GET              /api/events/stream                               api_events_stream
 12155  GET              /api/health                                      api_health
 20939  POST             /api/highlights/config                           api_highlights_config
 11231  POST             /api/login                                       dashboard_login_submit
 13037  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12225  GET              /api/notify/status                               api_notify_status
 12236  POST             /api/notify/test                                 api_notify_test
 12873  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12850  GET              /api/proxy/trend                                 api_proxy_trend
 21026  GET              /api/tts/<fn>                                    api_tts_file
 21803  GET              /api/upload_window                               api_upload_window
 12398  GET              /archive/<int:eid>/download                      archive_download
 12424  GET              /download/<int:recording_id>                     download
 12357  GET              /health                                          health
 20780  GET              /healthz                                         healthz
 11222  GET              /login                                           dashboard_login_page
 11256  GET              /logout                                          dashboard_logout
 11263  GET              /manifest.webmanifest                            pwa_manifest
 21784  GET              /overlay                                         overlay_page
 11287  GET              /pwa-icon-<variant>.png                          pwa_icon
 11273  GET              /sw.js                                           pwa_service_worker
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
   532  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   811  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   678  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   661  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   653  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   466  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   482  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   855  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   384  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   415  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   820  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   840  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   712  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
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
  2599  /about                  Ueber diesen Bot
  1165  /ai                     
  2599  /aireset                KI-Kontext zuruecksetzen
  1598  /ask                    
  1266  /assign_role            
  1316  /ban                    
  2555  /botstats               
  2599  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2599  /bulkadd                Mehrere User auf einmal tracken · a b c
  2599  /cleanup                Alte Aufnahmen aufraeumen
  1864  /clearwarns             
  2519  /clip                   
  2504  /clipoftheweek          
  1734  /clips                  
  2599  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1221  /create_category        
  1192  /create_channel         
  1256  /create_group           
  1231  /create_role            
  1207  /create_voice           
  1475  /daily                  
  2599  /diag                   Vollstaendige Diagnose
  2599  /einnahmen              Einnahmen und Spenden
  1627  /event                  
  1669  /events                 
  1774  /follow                 
  1763  /help                   
  1306  /kick                   
  1447  /leaderboard            
  2599  /live                   Live-Status sofort pruefen · @user
  1721  /livenow                
  2599  /logs                   Letzte Fehler aus dem Log
  2599  /pause                  Tracking pausieren · @user
  1749  /post_test              
  1559  /profile                
  1338  /purge                  
  2599  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2599  /quota                  Speicher-Quota
  1434  /rank                   
  1709  /recstatus              
  1276  /remove_role            
  2599  /report                 Azrael-Sentinel-Wochenreport
  1178  /restream_status        
  2599  /resume                 Tracking fortsetzen · @user
  1286  /set_channel_perms      
  1398  /setup_community        
  1415  /setup_targets          
  1695  /spenden                
  1806  /stats                  
  1137  /status                 
  2599  /stoprec                Laufende Aufnahme sauber beenden · @user
  1902  /streaminfo             
  2599  /summary                Tageszusammenfassung
  2599  /sysres                 System-Ressourcen
  2599  /teststream             Recorder-Selbsttest · @user
  2599  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1326  /timeout                
  1874  /topstreamers           
  2599  /topusers               Top-Streamer nach Aufnahmen
  1067  /track                  
  2599  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
  1150  /tracklist              
  1788  /unfollow               
  2599  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
  1099  /untrack                
  1827  /warn                   
  1850  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2703  on_member_join
  2660  on_message
  2620  on_raw_reaction_add
  2738  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    59-74     konfiguriere
    77-543    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (65 Funktionen)

```
  2009-2060   _award_xp
  1352-1368   _bereiche_bericht
   548-559    _clip_kopieren
  2225-2254   _clip_week_leader
  2278-2289   _clipoftheweek_loop
   659-712    _clips_einsortieren
  2855-2917   _community_events_loop
   358-367    _dc_abbruch_melden
  1979-1985   _dc_bereit
  1936-1958   _dc_client
   341-355    _dc_fehlerart
  1961-1970   _dc_offen
  1988-2000   _dc_warten
  2957-2992   _disc_automod_check
   474-479    _disc_sprache_setzen
  2063-2111   _discord_ai_automod
   870-909    _discord_automod
  2114-2134   _discord_azrael_reply
  2424-2814   _discord_run_once
   248-325    _discord_start
   370-424    _ensure_discord_invite
  2820-2852   _ensure_error_channel
   495-508    _ensure_rank_roles
  1030-1044   _ensure_team_roles
  2920-2950   _error_channel_loop
   602-606    _getrackte_nutzer
   919-923    _guard
   803-867    _handle_voice_ai
   482-492    _is_admin
   574-599    _link_video
  2179-2187   _liveboard_loop
   926-959    _on_level_up
   740-741    _par_chat_id
  2257-2275   _post_clip_of_week
  2190-2208   _post_weekly_digest
   511-537    _provision_base_channels
  1701-1795   _reg_betrieb
  1371-1464   _reg_community_setup
  1467-1548   _reg_daily_profil
  1591-1688   _reg_frage_events
  1124-1180   _reg_info
  1298-1349   _reg_moderation
  1551-1588   _reg_profil
  1247-1295   _reg_rollen
  1183-1244   _reg_server
  1691-1698   _reg_spenden
  1798-1885   _reg_streamer
  1888-1933   _reg_system
  1058-1121   _reg_tracking
   994-1027   _run_tg_handler
  2387-2411   _stern_an_telegram
  2414-2421   _stern_anspruch_zurueck
  2292-2384   _stern_highlight
   165-227    _uebernehmen
   562-571    _umzugsmarken
  2143-2176   _update_liveboard
   789-800    _voice_dauer
   760-767    _voice_max_s
   770-786    _voice_zulassen
  2211-2222   _weekly_digest_loop
   540-545    _ziel_guild
   609-656    _ziele_abgleichen
   721-737    _ziele_sync_loop
   715-718    _ziele_takt_min
   230-233    starte
```

## Top-Level-Symbole in bot.py (591 Funktionen, 4 Klassen)

```
 26643-26665  _abbruch_datenbank_unlesbar
  2845-2846   _abo_key
  2866-2884   _abo_probe_dump
 26765-26781  _abschied_wachen
 26784-26802  _abschluss
 16990-16997  _ad_allowlist
 18156-18162  _agent_for
 18165-18181  _ai_telemetry
 18697-18715  _alert
 22224-22274  _alert_monitor_loop
 19402-19459  _alte_beilagen_einsammeln
 22661-22723  _announce_loop
  3796-3806   _anthropic_key
  3809-3811   _anthropic_model
 10754-10757  _arg_int
  2837-2842   _as_dict
 26329-26338  _async_exc_handler
 18886-18908  _audio_tap_cmd
 19928-19987  _audio_tap_melden
 18922-18946  _audio_tap_sammler
 10101-10138  _aufnahme_beim_stopp_sichern
 19344-19365  _aufnahme_chat_ausklang
 19328-19341  _aufnahme_chat_beginnen
 19487-19508  _aufnahme_chat_dienst
 19686-19741  _aufnahme_chat_einarbeiten
 19323-19325  _aufnahme_chat_modus
 19511-19560  _aufnahme_chat_nachtrag
 19368-19399  _aufnahme_chat_vormerken
 19478-19484  _aufnahme_chat_wecken
 25445-25447  _aufnahme_deckel
 19563-19584  _aufnahme_fertigmachen
 22907-22968  _aufnahme_nach_discord
 10141-10159  _aufnahme_platz_frei
 10044-10071  _aufnahme_verteilen
 26729-26749  _aufnahmen_abschliessen
 26668-26726  _aufraeumen
 11043-11112  _auth_cookie
 10997-11039  _auth_guard
  2092-2097   _auto_on
 20643-20669  _auto_restream_loop
 14304-14346  _avatar_frames_laden
 17040-17053  _azrael_brain_kontext
 23879-23894  _azrael_broadcast_reply
 23779-23801  _azrael_chat_reply
 23751-23776  _azrael_chat_should_reply
 23807-23809  _azrael_gate_cfg
  4340-4355   _azrael_ki
 18184-18198  _azrael_live_state
  4358-4381   _azrael_lokal
 21670-21684  _azrael_overlay_state
 18240-18248  _azrael_persona_kern
 18579-18633  _azrael_proactive_loop
 18004-18060  _azrael_reaction_to_chats
 23812-23819  _azrael_reply_all_chats
  4384-4399   _azrael_schweigt_melden
 23738-23748  _azrael_self_names
 23847-23876  _azrael_send_to
 14265-14301  _azrael_spricht
 14623-14636  _azrael_stimme_stumm
 18204-18237  _azrael_system
 22358-22361  _backup_active
 22439-22452  _backup_loop
  5583-5606   _betreiber_pruefen
 25534-25538  _betrieb
 26402-26411  _brain_crowdsec_snap
 26570-26573  _brain_db_health
 24736-24776  _brain_fragen
 22145-22154  _brain_growth_loop
 11430-11457  _brain_growth_snapshot
  2756-2790   _brain_hint_delay
 26474-26509  _brain_moderation_snap
  6903-6931   _brain_notify
 26576-26598  _brain_recording_snap
 26414-26471  _brain_restream_health
 26601-26614  _brain_tiktok_status_snap
 12271-12292  _browser_push
 14670-14674  _build_restream_cmd
  5609-5636   _can_stop_tracking
  2203-2225   _capture_set_cookies
 12903-12906  _cfg_get
 12909-12911  _cfg_set
 21381-21416  _channel_set_all
 13346-13349  _chat_connected
 13352-13368  _chat_disconnected
 19472-19475  _chat_einarbeiten_async
  9535-9565   _chat_is_forum
 19292-19317  _chat_listener_abbauen
  9707-9742   _chat_migriert
  9745-9746   _chat_migriert_async
 13382-13384  _chat_sanitize
 13331-13343  _chat_stat
  4214-4226   _check_ai_models_sync
 11625-11668  _classify_pool_anonymity
   920-942    _claude_chat_sync_metered
 10799-10805  _client_ip
 23380-23394  _clip_chat_ass
 22807-22850  _clip_prune
 22853-22863  _clip_recfile_for
 23294-23368  _clip_schneiden
 23397-23403  _clip_should_velocity
 22971-23057  _clip_to_discord
 19657-19662  _clips_abwarten
  3996-4005   _close_ai_session
 23925-23940  _cohost_broadcast
 23910-23911  _cohost_cfg
 23966-23978  _cohost_fire_highlight
 23914-23922  _cohost_gate
 23943-23963  _cohost_highlight
  7233-7294   _cookie_alarm_loop
  2293-2294   _cookie_autofetch_info
  2277-2281   _cookie_autorefresh_info
 25999-26021  _cookie_bezug_loop
 26024-26049  _cookie_bezug_runde
  2180-2184   _cookie_header
 10808-10813  _cookie_sicher
  2306-2320   _cookies_selbst_holen
  4489-4491   _create_index_safe
  7119-7146   _daily_summary_loop
  3322-3347   _darf_ytdlp_nachschlagen
 12439-12460  _dashboard_adresse
 10828-10832  _dashboard_hostnamen
  1536-1566   _dashboard_trackings_umziehen
 23371-23377  _datei_weg
 22198-22221  _db_maintenance_loop
  7069-7116   _db_vacuum_loop
 12463-12472  _deck_intern_url
 17013-17037  _detect_foreign_ad
  1773-1784   _diag_path_owner
 18484-18529  _director_finalize
 19918-19925  _director_for
 18433-18481  _director_mark
 23207-23210  _disc_state_get
 23213-23220  _disc_state_set
 22126-22135  _discord_bot_starten
 22089-22100  _discord_einladung_merken
 22138-22142  _discord_invite
 22103-22123  _discord_kontext
 23168-23204  _discord_live_thread
 18636-18648  _discord_notify
 22061-22086  _discord_ops_alert
 23068-23164  _discord_post_user
 22726-22732  _discord_stop
  7149-7230   _disk_alarm_loop
 25870-25921  _disk_autoclean
 26185-26198  _disk_guard_loop
 14244-14251  _drossel_hoeher
 14240-14241  _drossel_stufe
 14254-14262  _drossel_zuruecksetzen
 12641-12643  _dump_all_threads
 25541-25555  _einstellungen_startzeile
  2345-2406   _ensure_cookie_file_netscape
  9636-9639   _ensure_notify_topic
 11775-11812  _ensure_proxy_ready
  9575-9598   _ensure_topic
   763-765    _env_int
   768-770    _env_int_range
 18681-18694  _event_webhook
 13129-13142  _evolution_loop
  6309-6343   _extract_file_payload
  1522-1533   _fanout_ziele
 26805-26870  _fatal_vom_botteil
 25450-25465  _fd_grenze_anheben
  5166-5176   _fehler_text
 11524-11542  _fetch_proxy_list
 19261-19289  _fetch_tiktok_room_id
   848-851    _ff_cmd
 19670-19683  _ffprobe_masse
 14168-14184  _fifo_schreiber_wecken
 13956-13961  _find_chromium
  3717-3719   _find_external_recorder
  2469-2471   _find_stream_urls
 12952-12977  _fire_webhooks
  8182-8192   _fork_safe
   953-966    _freeai_chat_sync_metered
  3984-3993   _get_ai_session
  8010-8050   _get_live_info
  3166-3173   _get_resolve_semaphore
  8707-9142   _handle_single_tracking
 25654-25656  _hb
 25659-25676  _hb_while
 20893-20904  _healthz_fuer_aufrufer
 25700-25728  _heap_zurueckgeben
 11116-11133  _herkunft_guard
 13396-13398  _highlight_cfg
 13401-13430  _highlight_observe
 12475-12485  _htmlov_basis_url
 14028-14036  _htmlov_bild_schreiben
 13997-14025  _htmlov_dauerbrowser
 13976-13994  _htmlov_screenshot_cmd
 13964-13973  _htmlov_url
 18948-18958  _httpx_proxy
 12985-12997  _in_quiet_hours
 26629-26640  _init_db_oder_abbruch
 27484-27515  _install_fast_eventloop
 10649-10703  _install_fast_json
 12646-12662  _install_faulthandler
 20689-20698  _intel_ensure_schema
 20741-20776  _intel_index_loop
 20710-20725  _intel_index_one
 20701-20707  _intel_semantic
  5568-5581   _is_authorized
  8533-8554   _is_dead
  1992-1999   _is_process_running
  6933-6940   _is_quiet_hours
  1411-1420   _is_upload_window
  4998-5013   _iso
 10816-10825  _ist_lokal
 10738-10751  _json_error_handler
  4058-4077   _ki_nach_deckwahl
  4135-4144   _ki_rueckfall_melden
  8408-8415   _kick_cluster_gefunden
  8343-8405   _kick_cluster_weiter
  6982-7024   _kick_follower_count
  6966-6969   _kick_slug
  8313-8340   _kick_ws_pause
 26617-26626  _kickmod_boot
 25965-25968  _lagebild_discord_aufnahme
 25978-25982  _lagebild_kick_chat
 25971-25975  _lagebild_overlay
 25985-25987  _lagebild_spendenziel
 25952-25962  _lagebild_upload
 13014-13016  _latest_popularity
  1929-1938   _laufstand
 26140-26182  _laufstand_loop
 25578-25616  _leistung_erheben
  7899-7926   _link_video_senden
  8694-8705   _live_check_frist_melden
  2900-2913   _live_ohne_stream
 20326-20375  _live_react_loop
 19990-20312  _live_react_worker
  3565-3679   _live_status_aufloesen
 18063-18074  _live_transcript_push
 20314-20324  _live_users
 18532-18576  _living_title_loop
 22364-22436  _local_backup_scan
  4932-4961   _lock_update
 10720-10734  _log_5xx
 25619-25651  _log_schleuse_pruefen
   838-845    _log_sicher
 14682-14694  _looks_like_codec_err
 14677-14679  _looks_like_source_expired
  8231-8261   _loop_fehler
 12665-12674  _loop_heartbeat
 25356-25389  _loop_lag_monitor
 25403-25423  _loop_stockung_melden
 25426-25436  _loop_takt_starten
 12677-12750  _loop_watchdog_thread
 17940-17957  _loyalty_add
 17931-17937  _loyalty_get
 17960-17968  _loyalty_top
  5277-5296   _manual_status
  8556-8557   _mark_dead
 11995-12011  _marketing_loop
 23826-23844  _maybe_handle_command
 26284-26308  _maybe_hype_clip
 22776-22804  _meme_klassifizieren
 19587-19654  _meme_zusammenschnitt
  4476-4481   _migrate_columns
 24108-24119  _mod_is_exempt
 24122-24127  _mod_warn_first
 24130-24133  _mod_warn_text
 13171-13190  _modlog
 13154-13168  _modlog_schreiben
  1104-1106   _multistream_targets
  3350-3386   _nachschlag_ytdlp
  8195-8196   _nc_create_subprocess_exec
  8199-8200   _nc_create_subprocess_shell
 12109-12126  _news_loop
 13213-13215  _normalize_ingest
  2687-2704   _note_check_duration
  9630-9633   _notify_topic_name
  4080-4085   _nur_free
  4088-4092   _nur_free_sync
  4095-4132   _nur_lokal_sync
  2891-2897   _offline_ergebnis
  3389-3412   _ohne_url_melden
 18089-18097  _oracle_memories
 18384-18418  _oracle_memorize
 18100-18113  _oracle_persona
 18082-18086  _oracle_recent_text
 13619-13620  _ov_atomic_write
 13610-13612  _ov_bar
 16918-16930  _ov_clip_text
 13615-13616  _ov_oneline
 13709-13770  _overlay_kanalweit
 21719-21777  _overlay_push
 13910-13953  _overlay_render_size
 13773-13800  _overlay_sendebild_schreiben
 13282-13286  _overlay_session_reset
 21686-21688  _overlay_src_ok
 13629-13641  _overlay_takt
 17000-17010  _own_invites
 13905-13907  _parse_size
  7544-7577   _pause_resume_cmd
  2231-2275   _persist_refreshed_cookies
  2134-2166   _pick_checked_pull_proxy
 10882-10897  _pin_auth_value
 10986-10987  _pin_clear_fail
 10950-10953  _pin_global_gesperrt
 10903-10914  _pin_hmac_schluessel
 10956-10963  _pin_locked
 10966-10983  _pin_note_fail
 10917-10938  _pin_ok
 21514-21539  _piper_pick_model
 21599-21664  _piper_say
 12914-12949  _post_json_threaded
 13884-13902  _probe_video_size
  2020-2037   _proc_is_recorder
 11744-11772  _proxy_pool_refresh_loop
  2100-2131   _proxy_report_recording
  9281-9365   _pruef_runde
  9240-9278   _pruefstand_melden
 25485-25496  _pruefung_verworfen
 12631-12633  _prune_stall_dumps
  2297-2303   _pull_proxy_still
 18652-18678  _push_notify
 11180-11182  _pwa_dir
 11593-11610  _quick_validate_proxy
 12980-12982  _quiet_hours_config
 11145-11178  _rate_guard
  2916-2944   _raumsperre_fragen
 17901-17907  _react_warn
  8097-8136   _reap_proc
 10835-10851  _rebinding_melden
  9974-10041  _rec_auto_abschalten
  9921-9971   _rec_frueh_getrennt
  9786-9866   _rec_kategorie_melden
  9869-9918   _rec_totstreak_fortschreiben
  2727-2749   _record_check_outcome
   833-835    _redact_stream_urls
 11671-11741  _refresh_proxy_pool
  2504-2595   _resolve_via_html
  2947-3143   _resolve_via_webcast_api_v2
  3211-3298   _resolve_via_ytdlp
 23437-23566  _resolve_youtube_ingest
  2480-2501   _resolver_stumm
 13265-13276  _restream_active_sources
 14349-14487  _restream_avatar_feeder_start
 14490-14500  _restream_avatar_feeder_stop
 19744-19882  _restream_chat_guardian
 13433-13518  _restream_chat_push
 13595-13605  _restream_chat_push_async
 14187-14204  _restream_chatbild_start
 26512-26567  _restream_durchreicher
 14039-14165  _restream_html_overlay_start
 14207-14227  _restream_html_overlay_stop
 20627-20640  _restream_liste_abgleichen
 13224-13247  _restream_overlay_files
 20378-20410  _restream_platform_state
 20586-20621  _restream_resume_after_restart
 13549-13566  _restream_soll_schreiben
 13569-13592  _restream_status_schreiben
 14548-14620  _restream_tts_enqueue_wav
 13846-13878  _restream_tts_feeder
 13843-13844  _restream_tts_fifo_path
 14503-14530  _restream_tts_start
 14532-14546  _restream_tts_stop
 20416-20583  _restream_verify_loop
 22329-22341  _retention_loop
 22323-22326  _retention_scan
  2848-2850   _room_is_abo
  6346-6501   _run_ai_call
 12773-12786  _run_async_from_flask
 27473-27481  _run_selfcheck_and_exit
 22344-22355  _s3_client
  8583-8653   _safe_send
  5240-5256   _sample_net_throughput
 27453-27470  _sc_bericht
 27394-27450  _sc_dienste
 27301-27391  _sc_ki_und_stimme
 27252-27298  _sc_umgebung
  2793-2823   _schedule_next_check
 22277-22320  _scheduler_loop
  4484-4486   _schema_pk
 12789-12794  _scraper_session
 24136-24175  _screen_full
 12171-12208  _sec_headers
  2464-2466   _select_stream_from_data_section
 27162-27249  _selfcheck
  9642-9676   _send_live_notice
  1434-1438   _should_defer_upload
 22866-22904  _shrink_for_discord
 11185-11218  _sicheres_ziel
 22157-22195  _sicherheits_erinnerung_loop
 26205-26222  _sign_health_check
 26225-26244  _sign_health_loop
  5016-5046   _sitzung_bestimmen
 20876-20886  _sparen_lage
  8212-8223   _spawn
 27906-27936  _spawn_from_flask
 25499-25505  _speicher_maps
 25508-25523  _speicher_pflegen
 18960-19258  _start_chat_listener
 25468-25482  _start_gesperrt
 12753-12770  _start_loop_watchdog
 12057-12106  _stats_loop
 12036-12039  _stats_output_path
 12042-12054  _stats_write
 21551-21565  _stimme_saubern
 21572-21596  _stimme_schon_gesagt
  9221-9237   _storage_cleanup_loop
 26264-26271  _story_for
  3741-3747   _stream_url_expiry
  3749-3754   _stream_url_ttl
 16963-16970  _streamer_persona_get
 22461-22619  _system_backup
 22628-22658  _system_backup_loop
 12591-12609  _task_auf_bot_schleife
 25013-25029  _telegram_befehlsmenue
  8264-8310   _telegram_polling_fehler
 25045-25080  _telegram_starten
  1492-1519   _telegram_ziele
 11545-11584  _test_proxy
 11967-11983  _testpush_resolve_live
 19665-19667  _text_schreiben
  7866-7874   _tg_botname
  7824-7863   _tg_ki_dialog
  9694-9704   _tg_migriert_laden
  9690-9691   _tg_migriert_pfad
  8559-8580   _tg_sprache_setzen
  9504-9514   _tg_topics_load_into_mem
  9501-9502   _tg_topics_path
  9516-9523   _tg_topics_save
 10854-10864  _token_ok
  9601-9617   _topic_anlegen
  9526-9533   _topic_forget
 13000-13011  _tracking_max_duration
  4746-4760   _tracking_remove_cleanup
  4777-4789   _tracking_resume_cleanup
  1831-1854   _try_attach_file_handler
 21541-21549  _tts_cleanup
 25924-25944  _tunnel_lage
 26085-26137  _tunnel_wacht_loop
 21044-21097  _twitch_channel_status
 24178-24326  _twitch_chat_loop
 23226-23239  _twitch_clip_versuchen
 23989-24095  _twitch_eventsub_loop
  1619-1656   _upload_queue_abarbeiten
  1470-1490   _upload_queue_add
  1584-1592   _upload_queue_count
  1440-1444   _upload_queue_load
  1659-1681   _upload_queue_nachher
  1430-1432   _upload_queue_path
  1569-1573   _upload_queue_remove
  1464-1468   _upload_queue_save
  1447-1462   _upload_queue_schreibbar
  1576-1582   _upload_queue_update
 10074-10098  _upload_rest_sichern
  1594-1616   _upload_window_loop
  8070-8077   _uptime_s
 13201-13210  _url_host
  3415-3513   _url_nachschlag
   913-917    _usage_record_claude
 26377-26399  _v37_pause_source
 26341-26351  _v37_restream_restart
 26354-26374  _v37_unpause_source
  8482-8526   _verbindung_verloren
  7027-7058   _viewer_sample_loop
 10990-10993  _wants_html
  8080-8094   _warn_empty_env
 25731-25856  _watchdog_loop
 23710-23718  _wchat_thank_ok
 26052-26082  _werkzeug_wacht_loop
 18720-18758  _whisper_get_model
  8171-8179   _whisper_native_section
 17888-17894  _whisper_pool
 18852-18884  _whisper_segments
 18760-18776  _whisper_stumm
 18779-18849  _whisper_transcribe
 13682-13706  _write_restream_overlay
 13644-13679  _write_restream_overlay_async
 24350-24449  _youtube_api_chat_loop
 21100-21203  _youtube_api_status
 21206-21273  _youtube_channel_status
 24452-24616  _youtube_chat_loop
 23242-23267  _youtube_clip_versuchen
 23572-23585  _youtube_restream_autoconfig
 23588-23612  _youtube_restream_autoconfig_inner
 23679-23707  _youtube_send
 21337-21378  _youtube_set_channel
 23615-23649  _yt_access_token
 23652-23667  _yt_live_chat_id
 23675-23676  _yt_sendrate_cfg
 24329-24344  _yt_timeout
  3190-3191   _ytdlp_detect_available
  3206-3208   _ytdlp_einzeln
  3193-3204   _ytdlp_note_result
 12636-12638  _zombie_child_count
 25558-25575  _zustand_kennzahlen
  7946-7970   about
  4665-4669   add_ai_log_entry
  5054-5148   add_recording
  4721-4738   add_tracking
  6504-6537   ai
  4235-4332   ai_chat
  4431-4441   ai_history_append
  4443-4448   ai_history_clear
  4420-4429   ai_history_load
  4405-4418   ai_rate_limit_check
  6566-6574   aireset
 18251-18270  azrael_chat
 24621-24724  brain_cmd
  3757-3762   build_recording_cmd
  4741-4744   bulk_add_trackings
  7297-7356   bulkadd
  9368-9484   check_all_trackings
  4792-4804   claim_live_transition
 17056-17820  class KickModerator
 14697-16806  class RestreamManager
  4964-4965   class _AufnahmeLockVerloren
  8418-8479   class _KickClusterSuche
 11855-11897  classify_proxy_anonymity
  6612-6809   cleanup
  5509-5515   cleanup_old_recordings
  4989-4996   clear_recording
 23270-23291  clip_moment
  7419-7495   cookies_cmd
  7498-7541   cookies_datei_cmd
  4712-4718   count_trackings_for_chat
  4652-4663   decide_preferred_recorder
  6004-6151   diag
 24895-24956  einnahmen_cmd
  4613-4629   finish_recording_attempt
  4765-4767   get_all_active_trackings
  5150-5153   get_all_recordings
  4591-4594   get_archive_entry
  2337-2342   get_cookie_health
  5220-5226   get_event_log
  4636-4650   get_last_recording_attempt
  3516-3558   get_live_status
  5231-5234   get_priority_poll_interval
  4631-4634   get_recent_recording_attempts
  5155-5158   get_recording_by_id
  3924-3953   get_redis
  5503-5507   get_storage_stats
  5270-5272   get_tiktok_status_distribution
  4806-4815   get_tracking_state
  4762-4763   get_trackings_for_group
 10162-10631  handle_recording_finished
 25005-25010  hilfe_cmd
  4499-4564   init_db
  5778-5816   live
  8656-8686   live_check_worker
  4008-4055   llm_chat
  4165-4206   llm_chat_sync
  4150-4162   llm_list_models
  5179-5212   log_event
  1954-1987   log_recording_failure
  7691-7740   logs_cmd
 26873-27152  main
  6540-6563   on_ai_media
  7817-7821   on_ai_reply
  7929-7943   on_azrael_mention
  7975-8005   on_callback
  9749-9767   on_chat_migration
  7883-7896   on_link_video
 18276-18381  oracle_handle
  7580-7583   pause_tracking
  5558-5563   profile_keyboard
  5731-5775   quelle
  7642-7688   quota
  9144-9218   reaper_loop
  5266-5268   record_tiktok_status
  6579-6609   recstatus
  3955-3963   redis_get_json
  3966-3972   redis_set_json
 25032-25042  report_cmd
 11900-11902  report_proxy_result
  2598-2640   resolve_tiktok_live_stream
  7586-7589   resume_tracking
 25083-25336  run_bot
 12488-12582  run_flask
  4672-4678   save_tiktok_check
  4968-4987   set_recording_file
  4770-4774   set_tracking_paused
 24990-25002  spenden_cmd
  9773-9784   split_and_send_video
  5641-5683   start
  4597-4611   start_recording_attempt
  6812-6850   stats
  5427-5480   stop_manual_recording
  7592-7639   stoprec
  6951-6959   summary_cmd
  7743-7814   sysres
  6153-6297   teststream
  5685-5726   tiktok
  7359-7416   topusers
  5853-5910   track
  5818-5850   track_exact
  5935-6002   tracklist
  5299-5425   trigger_manual_recording
  4894-4929   try_acquire_recording_lock
 24959-24987  unpause_cmd
  5912-5933   untrack
 24779-24892  update_cmd
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
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_cmd, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
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
discordaufnahme.py     an, beschriftung, hochladen, teilen
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
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
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
uploadschlange.py      angekommen, beiseite, class SchlangeUnlesbar, faellig, gleicher, lesen, nach_versuch, pause_s
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, in_arbeit, ist_kaputter_container, ist_rest, kopier_teilen, neu_kodieren, platz_reicht, reparieren, teile, teile_entfernen, wegwerfen, zeitstempel_richten, zu_gross
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
