# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11224  GET              /                                                dashboard
 12742  GET              /api/abo/status                                  api_abo_status
 12723  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11841  GET              /api/automation/status                           api_automation_status
 11863  POST             /api/automation/toggle                           api_automation_toggle
 21340  GET              /api/channel/categories                          api_channel_categories
 21346  POST             /api/channel/set                                 api_channel_set
 21197  GET              /api/channels/status                             api_channels_status
 20899  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20882  GET              /api/clips                                       api_clips
 20928  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20828  GET              /api/debug/threads                               api_debug_threads
 12728  GET              /api/events                                      api_events
 12219  GET              /api/events/stream                               api_events_stream
 12078  GET              /api/health                                      api_health
 20859  POST             /api/highlights/config                           api_highlights_config
 11154  POST             /api/login                                       dashboard_login_submit
 12960  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12148  GET              /api/notify/status                               api_notify_status
 12159  POST             /api/notify/test                                 api_notify_test
 12796  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12773  GET              /api/proxy/trend                                 api_proxy_trend
 20946  GET              /api/tts/<fn>                                    api_tts_file
 21723  GET              /api/upload_window                               api_upload_window
 12321  GET              /archive/<int:eid>/download                      archive_download
 12347  GET              /download/<int:recording_id>                     download
 12280  GET              /health                                          health
 20700  GET              /healthz                                         healthz
 11145  GET              /login                                           dashboard_login_page
 11179  GET              /logout                                          dashboard_logout
 11186  GET              /manifest.webmanifest                            pwa_manifest
 21704  GET              /overlay                                         overlay_page
 11210  GET              /pwa-icon-<variant>.png                          pwa_icon
 11196  GET              /sw.js                                           pwa_service_worker
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
   522  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   786  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   668  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   651  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   643  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   830  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   795  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   815  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   702  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
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
   976  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1117  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1145  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1165  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   963  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1025  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1012  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   993  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   638  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   633  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   681  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   564  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   891  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   655  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   618  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   591  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   865  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   735  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   824  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   663  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   454  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   908  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   542  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   786  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   941  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   926  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   498  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   725  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   711  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   694  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   751  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1308  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1429  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1272  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   844  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   740  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
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
   237  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   458  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   487  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   407  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   516  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   393  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   268  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   337  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   324  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   164  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   282  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   133  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   374  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   429  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
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
  2290  /about                  Ueber diesen Bot
  1009  /ai                     
  2290  /aireset                KI-Kontext zuruecksetzen
  1442  /ask                    
  1110  /assign_role            
  1160  /ban                    
  2246  /botstats               
  2290  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2290  /bulkadd                Mehrere User auf einmal tracken · a b c
  2290  /cleanup                Alte Aufnahmen aufraeumen
  1708  /clearwarns             
  2210  /clip                   
  2195  /clipoftheweek          
  1578  /clips                  
  2290  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1065  /create_category        
  1036  /create_channel         
  1100  /create_group           
  1075  /create_role            
  1051  /create_voice           
  1319  /daily                  
  2290  /diag                   Vollstaendige Diagnose
  2290  /einnahmen              Einnahmen und Spenden
  1471  /event                  
  1513  /events                 
  1618  /follow                 
  1607  /help                   
  1150  /kick                   
  1291  /leaderboard            
  2290  /live                   Live-Status sofort pruefen · @user
  1565  /livenow                
  2290  /logs                   Letzte Fehler aus dem Log
  2290  /pause                  Tracking pausieren · @user
  1593  /post_test              
  1403  /profile                
  1182  /purge                  
  2290  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2290  /quota                  Speicher-Quota
  1278  /rank                   
  1553  /recstatus              
  1120  /remove_role            
  2290  /report                 Azrael-Sentinel-Wochenreport
  1022  /restream_status        
  2290  /resume                 Tracking fortsetzen · @user
  1130  /set_channel_perms      
  1242  /setup_community        
  1259  /setup_targets          
  1539  /spenden                
  1650  /stats                  
   981  /status                 
  2290  /stoprec                Laufende Aufnahme sauber beenden · @user
  1746  /streaminfo             
  2290  /summary                Tageszusammenfassung
  2290  /sysres                 System-Ressourcen
  2290  /teststream             Recorder-Selbsttest · @user
  2290  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1170  /timeout                
  1718  /topstreamers           
  2290  /topusers               Top-Streamer nach Aufnahmen
   911  /track                  
  2290  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   994  /tracklist              
  1632  /unfollow               
  2290  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   943  /untrack                
  1671  /warn                   
  1694  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2457  on_member_join
  2414  on_message
  2311  on_raw_reaction_add
  2492  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    59-74     konfiguriere
    77-543    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (55 Funktionen)

```
  1823-1874   _award_xp
  1196-1212   _bereiche_bericht
   484-495    _clip_kopieren
  2045-2074   _clip_week_leader
  2098-2112   _clipoftheweek_loop
   595-648    _clips_einsortieren
  2609-2671   _community_events_loop
  1780-1802   _dc_client
  1805-1814   _dc_offen
  2711-2746   _disc_automod_check
   410-415    _disc_sprache_setzen
  1877-1925   _discord_ai_automod
   714-753    _discord_automod
  1928-1948   _discord_azrael_reply
  2115-2568   _discord_run_once
   245-303    _discord_start
   306-360    _ensure_discord_invite
  2574-2606   _ensure_error_channel
   431-444    _ensure_rank_roles
   874-888    _ensure_team_roles
  2674-2704   _error_channel_loop
   538-542    _getrackte_nutzer
   763-767    _guard
   683-711    _handle_voice_ai
   418-428    _is_admin
   510-535    _link_video
  1993-2004   _liveboard_loop
   770-803    _on_level_up
   679-680    _par_chat_id
  2077-2095   _post_clip_of_week
  2007-2025   _post_weekly_digest
   447-473    _provision_base_channels
  1545-1639   _reg_betrieb
  1215-1308   _reg_community_setup
  1311-1392   _reg_daily_profil
  1435-1532   _reg_frage_events
   968-1024   _reg_info
  1142-1193   _reg_moderation
  1395-1432   _reg_profil
  1091-1139   _reg_rollen
  1027-1088   _reg_server
  1535-1542   _reg_spenden
  1642-1729   _reg_streamer
  1732-1777   _reg_system
   902-965    _reg_tracking
   838-871    _run_tg_handler
   162-224    _uebernehmen
   498-507    _umzugsmarken
  1957-1990   _update_liveboard
  2028-2042   _weekly_digest_loop
   476-481    _ziel_guild
   545-592    _ziele_abgleichen
   657-676    _ziele_sync_loop
   651-654    _ziele_takt_min
   227-230    starte
```

## Top-Level-Symbole in bot.py (589 Funktionen, 4 Klassen)

```
 26514-26536  _abbruch_datenbank_unlesbar
  2823-2824   _abo_key
  2844-2862   _abo_probe_dump
 26636-26652  _abschied_wachen
 26655-26673  _abschluss
 16913-16920  _ad_allowlist
 18079-18085  _agent_for
 18088-18104  _ai_telemetry
 18620-18638  _alert
 22144-22194  _alert_monitor_loop
 19325-19382  _alte_beilagen_einsammeln
 22575-22637  _announce_loop
  3774-3784   _anthropic_key
  3787-3789   _anthropic_model
 10677-10680  _arg_int
  2815-2820   _as_dict
 26200-26209  _async_exc_handler
 18809-18831  _audio_tap_cmd
 19851-19910  _audio_tap_melden
 18845-18869  _audio_tap_sammler
 10024-10061  _aufnahme_beim_stopp_sichern
 19267-19288  _aufnahme_chat_ausklang
 19251-19264  _aufnahme_chat_beginnen
 19410-19431  _aufnahme_chat_dienst
 19609-19664  _aufnahme_chat_einarbeiten
 19246-19248  _aufnahme_chat_modus
 19434-19483  _aufnahme_chat_nachtrag
 19291-19322  _aufnahme_chat_vormerken
 19401-19407  _aufnahme_chat_wecken
 25325-25327  _aufnahme_deckel
 19486-19507  _aufnahme_fertigmachen
 22812-22873  _aufnahme_nach_discord
 10064-10082  _aufnahme_platz_frei
  9967-9994   _aufnahme_verteilen
 26600-26620  _aufnahmen_abschliessen
 26539-26597  _aufraeumen
 10966-11035  _auth_cookie
 10920-10962  _auth_guard
  2070-2075   _auto_on
 20563-20589  _auto_restream_loop
 14227-14269  _avatar_frames_laden
 16963-16976  _azrael_brain_kontext
 23784-23799  _azrael_broadcast_reply
 23684-23706  _azrael_chat_reply
 23656-23681  _azrael_chat_should_reply
 23712-23714  _azrael_gate_cfg
  4318-4333   _azrael_ki
 18107-18121  _azrael_live_state
  4336-4359   _azrael_lokal
 21590-21604  _azrael_overlay_state
 18163-18171  _azrael_persona_kern
 18502-18556  _azrael_proactive_loop
 17927-17983  _azrael_reaction_to_chats
 23717-23724  _azrael_reply_all_chats
  4362-4377   _azrael_schweigt_melden
 23643-23653  _azrael_self_names
 23752-23781  _azrael_send_to
 14188-14224  _azrael_spricht
 14546-14559  _azrael_stimme_stumm
 18127-18160  _azrael_system
 22278-22281  _backup_active
 22359-22372  _backup_loop
  5534-5557   _betreiber_pruefen
 25414-25418  _betrieb
 26273-26282  _brain_crowdsec_snap
 26441-26444  _brain_db_health
 24641-24681  _brain_fragen
 22065-22074  _brain_growth_loop
 11353-11380  _brain_growth_snapshot
  2734-2768   _brain_hint_delay
 26345-26380  _brain_moderation_snap
  6843-6871   _brain_notify
 26447-26469  _brain_recording_snap
 26285-26342  _brain_restream_health
 26472-26485  _brain_tiktok_status_snap
 12194-12215  _browser_push
 14593-14597  _build_restream_cmd
  5560-5587   _can_stop_tracking
  2181-2203   _capture_set_cookies
 12826-12829  _cfg_get
 12832-12834  _cfg_set
 21301-21336  _channel_set_all
 13269-13272  _chat_connected
 13275-13291  _chat_disconnected
 19395-19398  _chat_einarbeiten_async
  9458-9488   _chat_is_forum
 19215-19240  _chat_listener_abbauen
  9630-9665   _chat_migriert
  9668-9669   _chat_migriert_async
 13305-13307  _chat_sanitize
 13254-13266  _chat_stat
  4192-4204   _check_ai_models_sync
 11548-11591  _classify_pool_anonymity
   920-942    _claude_chat_sync_metered
 10722-10728  _client_ip
 23285-23299  _clip_chat_ass
 22721-22755  _clip_prune
 22758-22768  _clip_recfile_for
 23199-23273  _clip_schneiden
 23302-23308  _clip_should_velocity
 22876-22962  _clip_to_discord
 19580-19585  _clips_abwarten
  3974-3983   _close_ai_session
 23830-23845  _cohost_broadcast
 23815-23816  _cohost_cfg
 23871-23883  _cohost_fire_highlight
 23819-23827  _cohost_gate
 23848-23868  _cohost_highlight
  7173-7234   _cookie_alarm_loop
  2271-2272   _cookie_autofetch_info
  2255-2259   _cookie_autorefresh_info
 25875-25897  _cookie_bezug_loop
 25900-25925  _cookie_bezug_runde
  2158-2162   _cookie_header
 10731-10736  _cookie_sicher
  2284-2298   _cookies_selbst_holen
  4467-4469   _create_index_safe
  7059-7086   _daily_summary_loop
  3300-3325   _darf_ytdlp_nachschlagen
 12362-12383  _dashboard_adresse
 10751-10755  _dashboard_hostnamen
  1523-1553   _dashboard_trackings_umziehen
 23276-23282  _datei_weg
 22118-22141  _db_maintenance_loop
  7009-7056   _db_vacuum_loop
 12386-12395  _deck_intern_url
 16936-16960  _detect_foreign_ad
  1751-1762   _diag_path_owner
 18407-18452  _director_finalize
 19841-19848  _director_for
 18356-18404  _director_mark
 23112-23115  _disc_state_get
 23118-23125  _disc_state_set
 22046-22055  _discord_bot_starten
 22009-22020  _discord_einladung_merken
 22058-22062  _discord_invite
 22023-22043  _discord_kontext
 23073-23109  _discord_live_thread
 18559-18571  _discord_notify
 21981-22006  _discord_ops_alert
 22973-23069  _discord_post_user
 22640-22646  _discord_stop
  7089-7170   _disk_alarm_loop
 25746-25797  _disk_autoclean
 26056-26069  _disk_guard_loop
 14167-14174  _drossel_hoeher
 14163-14164  _drossel_stufe
 14177-14185  _drossel_zuruecksetzen
 12564-12566  _dump_all_threads
 25421-25435  _einstellungen_startzeile
  2323-2384   _ensure_cookie_file_netscape
  9559-9562   _ensure_notify_topic
 11698-11735  _ensure_proxy_ready
  9498-9521   _ensure_topic
   763-765    _env_int
   768-770    _env_int_range
 18604-18617  _event_webhook
 13052-13065  _evolution_loop
  6249-6283   _extract_file_payload
  1509-1520   _fanout_ziele
 26676-26739  _fatal_vom_botteil
 25330-25345  _fd_grenze_anheben
  5129-5139   _fehler_text
 11447-11465  _fetch_proxy_list
 19184-19212  _fetch_tiktok_room_id
   848-851    _ff_cmd
 19593-19606  _ffprobe_masse
 14091-14107  _fifo_schreiber_wecken
 13879-13884  _find_chromium
  3695-3697   _find_external_recorder
  2447-2449   _find_stream_urls
 12875-12900  _fire_webhooks
  8122-8132   _fork_safe
   953-966    _freeai_chat_sync_metered
  3962-3971   _get_ai_session
  7950-7990   _get_live_info
  3144-3151   _get_resolve_semaphore
  8647-9068   _handle_single_tracking
 25530-25532  _hb
 25535-25552  _hb_while
 20813-20824  _healthz_fuer_aufrufer
 25576-25604  _heap_zurueckgeben
 11039-11056  _herkunft_guard
 13319-13321  _highlight_cfg
 13324-13353  _highlight_observe
 12398-12408  _htmlov_basis_url
 13951-13959  _htmlov_bild_schreiben
 13920-13948  _htmlov_dauerbrowser
 13899-13917  _htmlov_screenshot_cmd
 13887-13896  _htmlov_url
 18871-18881  _httpx_proxy
 12908-12920  _in_quiet_hours
 26500-26511  _init_db_oder_abbruch
 27353-27384  _install_fast_eventloop
 10572-10626  _install_fast_json
 12569-12585  _install_faulthandler
 20609-20618  _intel_ensure_schema
 20661-20696  _intel_index_loop
 20630-20645  _intel_index_one
 20621-20627  _intel_semantic
  5519-5532   _is_authorized
  8473-8494   _is_dead
  1970-1977   _is_process_running
  6873-6880   _is_quiet_hours
  1411-1420   _is_upload_window
  4970-4985   _iso
 10739-10748  _ist_lokal
 10661-10674  _json_error_handler
  4036-4055   _ki_nach_deckwahl
  4113-4122   _ki_rueckfall_melden
  8348-8355   _kick_cluster_gefunden
  8283-8345   _kick_cluster_weiter
  6922-6964   _kick_follower_count
  6906-6909   _kick_slug
  8253-8280   _kick_ws_pause
 26488-26497  _kickmod_boot
 25841-25844  _lagebild_discord_aufnahme
 25854-25858  _lagebild_kick_chat
 25847-25851  _lagebild_overlay
 25861-25863  _lagebild_spendenziel
 25828-25838  _lagebild_upload
 12937-12939  _latest_popularity
  1907-1916   _laufstand
 26016-26053  _laufstand_loop
 25454-25492  _leistung_erheben
  7839-7866   _link_video_senden
  8634-8645   _live_check_frist_melden
  2878-2891   _live_ohne_stream
 20246-20295  _live_react_loop
 19913-20235  _live_react_worker
  3543-3657   _live_status_aufloesen
 17986-17997  _live_transcript_push
 20237-20244  _live_users
 18455-18499  _living_title_loop
 22284-22356  _local_backup_scan
  4910-4933   _lock_update
 10643-10657  _log_5xx
 25495-25527  _log_schleuse_pruefen
   838-845    _log_sicher
 14605-14617  _looks_like_codec_err
 14600-14602  _looks_like_source_expired
  8171-8201   _loop_fehler
 12588-12597  _loop_heartbeat
 25236-25269  _loop_lag_monitor
 25283-25303  _loop_stockung_melden
 25306-25316  _loop_takt_starten
 12600-12673  _loop_watchdog_thread
 17863-17880  _loyalty_add
 17854-17860  _loyalty_get
 17883-17891  _loyalty_top
  5240-5259   _manual_status
  8496-8497   _mark_dead
 11918-11934  _marketing_loop
 23731-23749  _maybe_handle_command
 26155-26179  _maybe_hype_clip
 22690-22718  _meme_klassifizieren
 19510-19577  _meme_zusammenschnitt
  4454-4459   _migrate_columns
 24013-24024  _mod_is_exempt
 24027-24032  _mod_warn_first
 24035-24038  _mod_warn_text
 13094-13113  _modlog
 13077-13091  _modlog_schreiben
  1104-1106   _multistream_targets
  3328-3364   _nachschlag_ytdlp
  8135-8136   _nc_create_subprocess_exec
  8139-8140   _nc_create_subprocess_shell
 12032-12049  _news_loop
 13136-13138  _normalize_ingest
  2665-2682   _note_check_duration
  9553-9556   _notify_topic_name
  4058-4063   _nur_free
  4066-4070   _nur_free_sync
  4073-4110   _nur_lokal_sync
  2869-2875   _offline_ergebnis
  3367-3390   _ohne_url_melden
 18012-18020  _oracle_memories
 18307-18341  _oracle_memorize
 18023-18036  _oracle_persona
 18005-18009  _oracle_recent_text
 13542-13543  _ov_atomic_write
 13533-13535  _ov_bar
 16841-16853  _ov_clip_text
 13538-13539  _ov_oneline
 13632-13693  _overlay_kanalweit
 21639-21697  _overlay_push
 13833-13876  _overlay_render_size
 13696-13723  _overlay_sendebild_schreiben
 13205-13209  _overlay_session_reset
 21606-21608  _overlay_src_ok
 13552-13564  _overlay_takt
 16923-16933  _own_invites
 13828-13830  _parse_size
  7484-7517   _pause_resume_cmd
  2209-2253   _persist_refreshed_cookies
  2112-2144   _pick_checked_pull_proxy
 10805-10820  _pin_auth_value
 10909-10910  _pin_clear_fail
 10873-10876  _pin_global_gesperrt
 10826-10837  _pin_hmac_schluessel
 10879-10886  _pin_locked
 10889-10906  _pin_note_fail
 10840-10861  _pin_ok
 21434-21459  _piper_pick_model
 21519-21584  _piper_say
 12837-12872  _post_json_threaded
 13807-13825  _probe_video_size
  1998-2015   _proc_is_recorder
 11667-11695  _proxy_pool_refresh_loop
  2078-2109   _proxy_report_recording
  9207-9288   _pruef_runde
  9166-9204   _pruefstand_melden
 25365-25376  _pruefung_verworfen
 12554-12556  _prune_stall_dumps
  2275-2281   _pull_proxy_still
 18575-18601  _push_notify
 11103-11105  _pwa_dir
 11516-11533  _quick_validate_proxy
 12903-12905  _quiet_hours_config
 11068-11101  _rate_guard
  2894-2922   _raumsperre_fragen
 17824-17830  _react_warn
  8037-8076   _reap_proc
 10758-10774  _rebinding_melden
  9897-9964   _rec_auto_abschalten
  9844-9894   _rec_frueh_getrennt
  9709-9789   _rec_kategorie_melden
  9792-9841   _rec_totstreak_fortschreiben
  2705-2727   _record_check_outcome
   833-835    _redact_stream_urls
 11594-11664  _refresh_proxy_pool
  2482-2573   _resolve_via_html
  2925-3121   _resolve_via_webcast_api_v2
  3189-3276   _resolve_via_ytdlp
 23342-23471  _resolve_youtube_ingest
  2458-2479   _resolver_stumm
 13188-13199  _restream_active_sources
 14272-14410  _restream_avatar_feeder_start
 14413-14423  _restream_avatar_feeder_stop
 19667-19805  _restream_chat_guardian
 13356-13441  _restream_chat_push
 13518-13528  _restream_chat_push_async
 14110-14127  _restream_chatbild_start
 26383-26438  _restream_durchreicher
 13962-14088  _restream_html_overlay_start
 14130-14150  _restream_html_overlay_stop
 20547-20560  _restream_liste_abgleichen
 13147-13170  _restream_overlay_files
 20298-20330  _restream_platform_state
 20506-20541  _restream_resume_after_restart
 13472-13489  _restream_soll_schreiben
 13492-13515  _restream_status_schreiben
 14471-14543  _restream_tts_enqueue_wav
 13769-13801  _restream_tts_feeder
 13766-13767  _restream_tts_fifo_path
 14426-14453  _restream_tts_start
 14455-14469  _restream_tts_stop
 20336-20503  _restream_verify_loop
 22249-22261  _retention_loop
 22243-22246  _retention_scan
  2826-2828   _room_is_abo
  6286-6441   _run_ai_call
 12696-12709  _run_async_from_flask
 27342-27350  _run_selfcheck_and_exit
 22264-22275  _s3_client
  8523-8593   _safe_send
  5203-5219   _sample_net_throughput
 27322-27339  _sc_bericht
 27263-27319  _sc_dienste
 27170-27260  _sc_ki_und_stimme
 27121-27167  _sc_umgebung
  2771-2801   _schedule_next_check
 22197-22240  _scheduler_loop
  4462-4464   _schema_pk
 12712-12717  _scraper_session
 24041-24080  _screen_full
 12094-12131  _sec_headers
  2442-2444   _select_stream_from_data_section
 27031-27118  _selfcheck
  9565-9599   _send_live_notice
  1434-1438   _should_defer_upload
 22771-22809  _shrink_for_discord
 11108-11141  _sicheres_ziel
 22077-22115  _sicherheits_erinnerung_loop
 26076-26093  _sign_health_check
 26096-26115  _sign_health_loop
  4988-5013   _sitzung_bestimmen
 20796-20806  _sparen_lage
  8152-8163   _spawn
 27775-27805  _spawn_from_flask
 25379-25385  _speicher_maps
 25388-25403  _speicher_pflegen
 18883-19181  _start_chat_listener
 25348-25362  _start_gesperrt
 12676-12693  _start_loop_watchdog
 11980-12029  _stats_loop
 11959-11962  _stats_output_path
 11965-11977  _stats_write
 21471-21485  _stimme_saubern
 21492-21516  _stimme_schon_gesagt
  9147-9163   _storage_cleanup_loop
 26135-26142  _story_for
  3719-3725   _stream_url_expiry
  3727-3732   _stream_url_ttl
 16886-16893  _streamer_persona_get
 22381-22533  _system_backup
 22542-22572  _system_backup_loop
 12514-12532  _task_auf_bot_schleife
 24911-24927  _telegram_befehlsmenue
  8204-8250   _telegram_polling_fehler
  1479-1506   _telegram_ziele
 11468-11507  _test_proxy
 11890-11906  _testpush_resolve_live
 19588-19590  _text_schreiben
  7806-7814   _tg_botname
  7764-7803   _tg_ki_dialog
  9617-9627   _tg_migriert_laden
  9613-9614   _tg_migriert_pfad
  8499-8520   _tg_sprache_setzen
  9427-9437   _tg_topics_load_into_mem
  9424-9425   _tg_topics_path
  9439-9446   _tg_topics_save
 10777-10787  _token_ok
  9524-9540   _topic_anlegen
  9449-9456   _topic_forget
 12923-12934  _tracking_max_duration
  4724-4738   _tracking_remove_cleanup
  4755-4767   _tracking_resume_cleanup
  1809-1832   _try_attach_file_handler
 21461-21469  _tts_cleanup
 25800-25820  _tunnel_lage
 25961-26013  _tunnel_wacht_loop
 20964-21017  _twitch_channel_status
 24083-24231  _twitch_chat_loop
 23131-23144  _twitch_clip_versuchen
 23894-24000  _twitch_eventsub_loop
  1599-1634   _upload_queue_abarbeiten
  1457-1477   _upload_queue_add
  1570-1572   _upload_queue_count
  1440-1449   _upload_queue_load
  1637-1659   _upload_queue_nachher
  1430-1432   _upload_queue_path
  1556-1560   _upload_queue_remove
  1451-1455   _upload_queue_save
  1563-1568   _upload_queue_update
  9997-10021  _upload_rest_sichern
  1574-1596   _upload_window_loop
  8010-8017   _uptime_s
 13124-13133  _url_host
  3393-3491   _url_nachschlag
   913-917    _usage_record_claude
 26248-26270  _v37_pause_source
 26212-26222  _v37_restream_restart
 26225-26245  _v37_unpause_source
  8422-8466   _verbindung_verloren
  6967-6998   _viewer_sample_loop
 10913-10916  _wants_html
  8020-8034   _warn_empty_env
 25607-25732  _watchdog_loop
 23615-23623  _wchat_thank_ok
 25928-25958  _werkzeug_wacht_loop
 18643-18681  _whisper_get_model
  8111-8119   _whisper_native_section
 17811-17817  _whisper_pool
 18775-18807  _whisper_segments
 18683-18699  _whisper_stumm
 18702-18772  _whisper_transcribe
 13605-13629  _write_restream_overlay
 13567-13602  _write_restream_overlay_async
 24255-24354  _youtube_api_chat_loop
 21020-21123  _youtube_api_status
 21126-21193  _youtube_channel_status
 24357-24521  _youtube_chat_loop
 23147-23172  _youtube_clip_versuchen
 23477-23490  _youtube_restream_autoconfig
 23493-23517  _youtube_restream_autoconfig_inner
 23584-23612  _youtube_send
 21257-21298  _youtube_set_channel
 23520-23554  _yt_access_token
 23557-23572  _yt_live_chat_id
 23580-23581  _yt_sendrate_cfg
 24234-24249  _yt_timeout
  3168-3169   _ytdlp_detect_available
  3184-3186   _ytdlp_einzeln
  3171-3182   _ytdlp_note_result
 12559-12561  _zombie_child_count
 25438-25451  _zustand_kennzahlen
  7886-7910   about
  4643-4647   add_ai_log_entry
  5021-5111   add_recording
  4699-4716   add_tracking
  6444-6477   ai
  4213-4310   ai_chat
  4409-4419   ai_history_append
  4421-4426   ai_history_clear
  4398-4407   ai_history_load
  4383-4396   ai_rate_limit_check
  6506-6514   aireset
 18174-18193  azrael_chat
 24526-24629  brain_cmd
  3735-3740   build_recording_cmd
  4719-4722   bulk_add_trackings
  7237-7296   bulkadd
  9291-9407   check_all_trackings
  4770-4782   claim_live_transition
 16979-17743  class KickModerator
 14620-16729  class RestreamManager
  4936-4937   class _AufnahmeLockVerloren
  8358-8419   class _KickClusterSuche
 11778-11820  classify_proxy_anonymity
  6552-6749   cleanup
  5460-5466   cleanup_old_recordings
  4961-4968   clear_recording
 23175-23196  clip_moment
  7359-7435   cookies_cmd
  7438-7481   cookies_datei_cmd
  4690-4696   count_trackings_for_chat
  4630-4641   decide_preferred_recorder
  5944-6091   diag
 24793-24854  einnahmen_cmd
  4591-4607   finish_recording_attempt
  4743-4745   get_all_active_trackings
  5113-5116   get_all_recordings
  4569-4572   get_archive_entry
  2315-2320   get_cookie_health
  5183-5189   get_event_log
  4614-4628   get_last_recording_attempt
  3494-3536   get_live_status
  5194-5197   get_priority_poll_interval
  4609-4612   get_recent_recording_attempts
  5118-5121   get_recording_by_id
  3902-3931   get_redis
  5454-5458   get_storage_stats
  5233-5235   get_tiktok_status_distribution
  4784-4793   get_tracking_state
  4740-4741   get_trackings_for_group
 10085-10554  handle_recording_finished
 24903-24908  hilfe_cmd
  4477-4542   init_db
  5729-5767   live
  8596-8626   live_check_worker
  3986-4033   llm_chat
  4143-4184   llm_chat_sync
  4128-4140   llm_list_models
  5142-5175   log_event
  1932-1965   log_recording_failure
  7631-7680   logs_cmd
 26742-27021  main
  6480-6503   on_ai_media
  7757-7761   on_ai_reply
  7869-7883   on_azrael_mention
  7915-7945   on_callback
  9672-9690   on_chat_migration
  7823-7836   on_link_video
 18199-18304  oracle_handle
  7520-7523   pause_tracking
  5509-5514   profile_keyboard
  5682-5726   quelle
  7582-7628   quota
  9070-9144   reaper_loop
  5229-5231   record_tiktok_status
  6519-6549   recstatus
  3933-3941   redis_get_json
  3944-3950   redis_set_json
 24930-24940  report_cmd
 11823-11825  report_proxy_result
  2576-2618   resolve_tiktok_live_stream
  7526-7529   resume_tracking
 24943-25216  run_bot
 12411-12505  run_flask
  4650-4656   save_tiktok_check
  4940-4959   set_recording_file
  4748-4752   set_tracking_paused
 24888-24900  spenden_cmd
  9696-9707   split_and_send_video
  5592-5634   start
  4575-4589   start_recording_attempt
  6752-6790   stats
  5378-5431   stop_manual_recording
  7532-7579   stoprec
  6891-6899   summary_cmd
  7683-7754   sysres
  6093-6237   teststream
  5636-5677   tiktok
  7299-7356   topusers
  5804-5861   track
  5769-5801   track_exact
  5875-5942   tracklist
  5262-5376   trigger_manual_recording
  4872-4907   try_acquire_recording_lock
 24857-24885  unpause_cmd
  5863-5873   untrack
 24684-24790  update_cmd
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
abwehrlage.py          auswerten, configure, crowdsec_status, crowdsec_via_lapi, cscli_bin, cscli_path, darf_journal_lesen, ssh_angriffe, sudo_hinweis
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, andere_kopien, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, dublette_loeschen, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            aus_bestand, config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_cmd, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, ist_zieldatei, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
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
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
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
revenue.py             is_revenue_platform, normalisieren, sql_in
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
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
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
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, text, zuruecksetzen
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
uploadschlange.py      angekommen, faellig, gleicher, nach_versuch, pause_s
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
