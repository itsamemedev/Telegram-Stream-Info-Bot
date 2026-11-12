# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11322  GET              /                                                dashboard
 13342  GET              /api/abo/status                                  api_abo_status
 13296  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 12083  GET              /api/automation/status                           api_automation_status
 12105  POST             /api/automation/toggle                           api_automation_toggle
 21974  GET              /api/channel/categories                          api_channel_categories
 21980  POST             /api/channel/set                                 api_channel_set
 21827  GET              /api/channels/status                             api_channels_status
 21501  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21484  GET              /api/clips                                       api_clips
 21530  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21402  GET              /api/debug/threads                               api_debug_threads
 13307  GET              /api/events                                      api_events
 12786  GET              /api/events/stream                               api_events_stream
 12613  GET              /api/health                                      api_health
 21443  POST             /api/highlights/config                           api_highlights_config
 11252  POST             /api/login                                       dashboard_login_submit
 13632  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12701  GET              /api/notify/status                               api_notify_status
 12712  POST             /api/notify/test                                 api_notify_test
 13396  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13373  GET              /api/proxy/trend                                 api_proxy_trend
 21550  GET              /api/tts/<fn>                                    api_tts_file
 22338  GET              /api/upload_window                               api_upload_window
 12903  GET              /archive/<int:eid>/download                      archive_download
 12931  GET              /download/<int:recording_id>                     download
 12860  GET              /health                                          health
 21274  GET              /healthz                                         healthz
 11243  GET              /login                                           dashboard_login_page
 11277  GET              /logout                                          dashboard_logout
 11284  GET              /manifest.webmanifest                            pwa_manifest
 22311  GET              /overlay                                         overlay_page
 11308  GET              /pwa-icon-<variant>.png                          pwa_icon
 11294  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (345)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1023  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   764  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   894  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   874  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   912  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   832  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   382  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   393  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   403  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   426  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   433  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   444  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   572  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   670  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1261  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1293  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   367  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   976  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   956  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1129  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1177  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1228  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1087  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   931  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
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
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   374  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   359  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   179  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   130  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    71  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    78  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   200  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   227  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   320  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   264  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   282  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   187  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   125  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   139  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   154  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   222  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   242  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   269  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
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
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
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
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
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
   229  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   212  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   121  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   539  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   591  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   613  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   552  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   578  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   415  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   405  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   440  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
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
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2285  /about                  Ueber diesen Bot
   981  /ai                     
  2285  /aireset                KI-Kontext zuruecksetzen
  1399  /ask                    
  1082  /assign_role            
  1132  /ban                    
  2240  /botstats               
  2285  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2285  /bulkadd                Mehrere User auf einmal tracken · a b c
  2285  /cleanup                Alte Aufnahmen aufraeumen
  1665  /clearwarns             
  2204  /clip                   
  2189  /clipoftheweek          
  1535  /clips                  
  2285  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1037  /create_category        
  1008  /create_channel         
  1072  /create_group           
  1047  /create_role            
  1023  /create_voice           
  1276  /daily                  
  2285  /diag                   Vollstaendige Diagnose
  2285  /einnahmen              Einnahmen und Spenden
  1428  /event                  
  1470  /events                 
  1575  /follow                 
  1564  /help                   
  1122  /kick                   
  1248  /leaderboard            
  2285  /live                   Live-Status sofort pruefen · @user
  1522  /livenow                
  2285  /logs                   Letzte Fehler aus dem Log
  2285  /pause                  Tracking pausieren · @user
  1550  /post_test              
  1360  /profile                
  1154  /purge                  
  2285  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2285  /quota                  Speicher-Quota
  1235  /rank                   
  1510  /recstatus              
  1092  /remove_role            
  2285  /report                 Azrael-Sentinel-Wochenreport
   994  /restream_status        
  2285  /resume                 Tracking fortsetzen · @user
  1102  /set_channel_perms      
  1197  /setup_community        
  1214  /setup_targets          
  1496  /spenden                
  1607  /stats                  
   953  /status                 
  2285  /stoprec                Laufende Aufnahme sauber beenden · @user
  1703  /streaminfo             
  2285  /summary                Tageszusammenfassung
  2285  /sysres                 System-Ressourcen
  2285  /teststream             Recorder-Selbsttest · @user
  2285  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1142  /timeout                
  1675  /topstreamers           
  2285  /topusers               Top-Streamer nach Aufnahmen
   883  /track                  
  2285  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   966  /tracklist              
  1589  /unfollow               
  2285  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   915  /untrack                
  1628  /warn                   
  1651  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2452  on_member_join
  2409  on_message
  2306  on_raw_reaction_add
  2487  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (54 Funktionen)

```
  1780-1831   _award_xp
   537-564    _bereich_umziehen
   484-494    _clip_kopieren
  2002-2031   _clip_week_leader
  2055-2069   _clipoftheweek_loop
  2604-2666   _community_events_loop
  1737-1759   _dc_client
  1762-1771   _dc_offen
  2706-2741   _disc_automod_check
   410-415    _disc_sprache_setzen
  1834-1882   _discord_ai_automod
   686-725    _discord_automod
  1885-1905   _discord_azrael_reply
  2072-2563   _discord_run_once
   245-303    _discord_start
   306-360    _ensure_discord_invite
  2569-2601   _ensure_error_channel
   431-444    _ensure_rank_roles
   846-860    _ensure_team_roles
  2669-2699   _error_channel_loop
   735-739    _guard
   655-683    _handle_voice_ai
   418-428    _is_admin
   509-534    _link_video
  1950-1961   _liveboard_loop
   742-775    _on_level_up
   651-652    _par_chat_id
  2034-2052   _post_clip_of_week
  1964-1982   _post_weekly_digest
   447-473    _provision_base_channels
  1502-1596   _reg_betrieb
  1168-1265   _reg_community_setup
  1268-1349   _reg_daily_profil
  1392-1489   _reg_frage_events
   940-996    _reg_info
  1114-1165   _reg_moderation
  1352-1389   _reg_profil
  1063-1111   _reg_rollen
   999-1060   _reg_server
  1492-1499   _reg_spenden
  1599-1686   _reg_streamer
  1689-1734   _reg_system
   874-937    _reg_tracking
   810-843    _run_tg_handler
   638-648    _tracked_usernames
   162-224    _uebernehmen
   497-506    _umzugsmarken
  1914-1947   _update_liveboard
  1985-1999   _weekly_digest_loop
   476-481    _ziel_guild
   567-609    _ziele_abgleichen
   618-635    _ziele_sync_loop
   612-615    _ziele_takt_min
   227-230    starte
```

## Top-Level-Symbole in bot.py (610 Funktionen, 4 Klassen)

```
 27518-27540  _abbruch_datenbank_unlesbar
  2831-2832   _abo_key
  2852-2870   _abo_probe_dump
 27640-27656  _abschied_wachen
 27659-27677  _abschluss
 17504-17511  _ad_allowlist
 18670-18676  _agent_for
 18679-18695  _ai_telemetry
 19215-19233  _alert
 23193-23243  _alert_monitor_loop
 19920-19977  _alte_beilagen_einsammeln
 23625-23687  _announce_loop
  3783-3793   _anthropic_key
  3800-3802   _anthropic_model
 10811-10814  _arg_int
  2823-2828   _as_dict
 27204-27213  _async_exc_handler
 19404-19426  _audio_tap_cmd
 20440-20499  _audio_tap_melden
 19440-19464  _audio_tap_sammler
 10157-10194  _aufnahme_beim_stopp_sichern
 19862-19883  _aufnahme_chat_ausklang
 19846-19859  _aufnahme_chat_beginnen
 20005-20026  _aufnahme_chat_dienst
 20199-20252  _aufnahme_chat_einarbeiten
 19841-19843  _aufnahme_chat_modus
 20029-20078  _aufnahme_chat_nachtrag
 19886-19917  _aufnahme_chat_vormerken
 19996-20002  _aufnahme_chat_wecken
 26328-26330  _aufnahme_deckel
 20081-20102  _aufnahme_fertigmachen
 23862-23915  _aufnahme_nach_discord
 10197-10215  _aufnahme_platz_frei
 10100-10127  _aufnahme_verteilen
 27604-27624  _aufnahmen_abschliessen
 27543-27601  _aufraeumen
 11085-11154  _auth_cookie
 11041-11081  _auth_guard
  2070-2075   _auto_on
 21126-21144  _auto_restream_loop
 14977-15019  _avatar_frames_laden
 17554-17567  _azrael_brain_kontext
 24821-24836  _azrael_broadcast_reply
 24721-24743  _azrael_chat_reply
 24693-24718  _azrael_chat_should_reply
 24749-24751  _azrael_gate_cfg
  4248-4261   _azrael_ki
 18700-18714  _azrael_live_state
  4264-4286   _azrael_lokal
 22224-22238  _azrael_overlay_state
 18756-18764  _azrael_persona_kern
 19097-19151  _azrael_proactive_loop
 18518-18574  _azrael_reaction_to_chats
 24754-24761  _azrael_reply_all_chats
  4289-4304   _azrael_schweigt_melden
 24680-24690  _azrael_self_names
 24789-24818  _azrael_send_to
 14938-14974  _azrael_spricht
 15285-15298  _azrael_stimme_stumm
 18720-18753  _azrael_system
 23327-23330  _backup_active
 23408-23421  _backup_loop
  5621-5644   _betreiber_pruefen
 26417-26421  _betrieb
 27277-27286  _brain_crowdsec_snap
 27445-27448  _brain_db_health
 23114-23123  _brain_growth_loop
 11495-11522  _brain_growth_snapshot
  2742-2776   _brain_hint_delay
 27349-27384  _brain_moderation_snap
  6895-6923   _brain_notify
 27451-27473  _brain_recording_snap
 27289-27346  _brain_restream_health
 27476-27489  _brain_tiktok_status_snap
 12765-12782  _browser_push
  6935-7022   _build_daily_summary
 15332-15336  _build_restream_cmd
  5647-5674   _can_stop_tracking
  2183-2205   _capture_set_cookies
 13450-13453  _cfg_get
 13456-13458  _cfg_set
 21935-21970  _channel_set_all
 14029-14032  _chat_connected
 14035-14051  _chat_disconnected
 19990-19993  _chat_einarbeiten_async
  9591-9621   _chat_is_forum
 19810-19835  _chat_listener_abbauen
  9763-9798   _chat_migriert
  9801-9802   _chat_migriert_async
 14071-14073  _chat_sanitize
 14014-14026  _chat_stat
 14054-14057  _chat_stats_snapshot
  4118-4130   _check_ai_models_sync
 11776-11819  _classify_pool_anonymity
   920-942    _claude_chat_sync_metered
 10843-10849  _client_ip
 24320-24334  _clip_chat_ass
 23771-23805  _clip_prune
 23808-23818  _clip_recfile_for
 24240-24308  _clip_schneiden
 24337-24343  _clip_should_velocity
 23918-24003  _clip_to_discord
 20170-20175  _clips_abwarten
  3987-3996   _close_ai_session
 24867-24882  _cohost_broadcast
 24852-24853  _cohost_cfg
 24908-24920  _cohost_fire_highlight
 24856-24864  _cohost_gate
 24885-24905  _cohost_highlight
 11431-11433  _conv_messages
  7319-7380   _cookie_alarm_loop
  2273-2274   _cookie_autofetch_info
  2257-2261   _cookie_autorefresh_info
 26878-26900  _cookie_bezug_loop
 26903-26928  _cookie_bezug_runde
  2160-2164   _cookie_header
 10852-10857  _cookie_sicher
  2286-2300   _cookies_selbst_holen
  4413-4415   _create_index_safe
 22663-22777  _crowdsec_status
 22609-22660  _crowdsec_via_lapi
 22520-22538  _cscli_bin
 22547-22560  _cscli_path
  7203-7230   _daily_summary_loop
 22578-22595  _darf_journal_lesen
  3308-3333   _darf_ytdlp_nachschlagen
 12946-12967  _dashboard_adresse
 10872-10876  _dashboard_hostnamen
  1522-1552   _dashboard_trackings_umziehen
 24311-24317  _datei_weg
 23167-23190  _db_maintenance_loop
  7153-7200   _db_vacuum_loop
 17527-17551  _detect_foreign_ad
  1750-1761   _diag_path_owner
 19002-19047  _director_finalize
 20429-20436  _director_for
 18951-18999  _director_mark
 24153-24156  _disc_state_get
 24159-24166  _disc_state_set
 23095-23104  _discord_bot_starten
 23058-23069  _discord_einladung_merken
 23107-23111  _discord_invite
 23072-23092  _discord_kontext
 24114-24150  _discord_live_thread
 19154-19166  _discord_notify
 23030-23055  _discord_ops_alert
 24014-24110  _discord_post_user
 23690-23696  _discord_stop
  7233-7314   _disk_alarm_loop
 26749-26800  _disk_autoclean
 27059-27072  _disk_guard_loop
 14916-14923  _drossel_hoeher
 14912-14913  _drossel_stufe
 14926-14934  _drossel_zuruecksetzen
 13123-13125  _dump_all_threads
 26424-26438  _einstellungen_startzeile
 11703-11766  _enrich_proxies_with_geo
  2329-2390   _ensure_cookie_file_netscape
  9692-9695   _ensure_notify_topic
 11926-11963  _ensure_proxy_ready
  9631-9654   _ensure_topic
   761-763    _env_int
   766-768    _env_int_range
 19199-19212  _event_webhook
 13797-13810  _evolution_loop
  6336-6370   _extract_file_payload
 22563-22570  _f2b_sudo_hint
  1508-1519   _fanout_ziele
 27680-27743  _fatal_vom_botteil
 26333-26348  _fd_grenze_anheben
  5087-5097   _fehler_text
 11604-11622  _fetch_proxy_list
 19779-19807  _fetch_tiktok_room_id
   846-849    _ff_cmd
 20183-20196  _ffprobe_masse
 14860-14876  _fifo_schreiber_wecken
 14670-14675  _find_chromium
  3703-3705   _find_external_recorder
  2455-2457   _find_stream_urls
 13501-13526  _fire_webhooks
  8252-8262   _fork_safe
   953-966    _freeai_chat_sync_metered
  3975-3984   _get_ai_session
  8080-8120   _get_live_info
  3152-3159   _get_resolve_semaphore
  8779-9200   _handle_single_tracking
 26533-26535  _hb
 26538-26555  _hb_while
 21387-21398  _healthz_fuer_aufrufer
 26579-26607  _heap_zurueckgeben
 11158-11175  _herkunft_guard
 14085-14087  _highlight_cfg
 14090-14119  _highlight_observe
 14721-14729  _htmlov_bild_schreiben
 14699-14718  _htmlov_dauerbrowser
 14678-14696  _htmlov_screenshot_cmd
 19466-19476  _httpx_proxy
 13534-13546  _in_quiet_hours
 27504-27515  _init_db_oder_abbruch
 28330-28361  _install_fast_eventloop
 10706-10760  _install_fast_json
 13128-13144  _install_faulthandler
 21177-21186  _intel_ensure_schema
 21229-21264  _intel_index_loop
 21198-21213  _intel_index_one
 21189-21195  _intel_semantic
  5606-5619   _is_authorized
  8605-8626   _is_dead
 22598-22600  _is_private_ip
  1969-1976   _is_process_running
  6925-6932   _is_quiet_hours
  1410-1419   _is_upload_window
  4952-4967   _iso
 10860-10869  _ist_lokal
 10795-10808  _json_error_handler
  4044-4053   _ki_rueckfall_melden
  7147-7148   _kick_broadcaster_id
  8480-8487   _kick_cluster_gefunden
  8415-8477   _kick_cluster_weiter
  7059-7101   _kick_follower_count
  7043-7046   _kick_slug
  8385-8412   _kick_ws_pause
 27492-27501  _kickmod_boot
  4497-4500   _kind_from_filename
 26844-26847  _lagebild_discord_aufnahme
 26857-26861  _lagebild_kick_chat
 26850-26854  _lagebild_overlay
 26864-26866  _lagebild_spendenziel
 26831-26841  _lagebild_upload
 13563-13565  _latest_popularity
  1906-1915   _laufstand
 27019-27056  _laufstand_loop
 26457-26495  _leistung_erheben
  7954-7981   _link_video_senden
  8766-8777   _live_check_frist_melden
  2886-2899   _live_ohne_stream
 20835-20884  _live_react_loop
 20502-20824  _live_react_worker
  3551-3665   _live_status_aufloesen
 18577-18588  _live_transcript_push
 20826-20833  _live_users
 19050-19094  _living_title_loop
 23333-23405  _local_backup_scan
  4892-4915   _lock_update
 10777-10791  _log_5xx
 26498-26530  _log_schleuse_pruefen
   836-843    _log_sicher
 15344-15356  _looks_like_codec_err
 15339-15341  _looks_like_source_expired
  8303-8333   _loop_fehler
 13148-13157  _loop_heartbeat
 26239-26272  _loop_lag_monitor
 26286-26306  _loop_stockung_melden
 26309-26319  _loop_takt_starten
 13160-13233  _loop_watchdog_thread
 18454-18471  _loyalty_add
 18445-18451  _loyalty_get
 18474-18482  _loyalty_top
  5288-5307   _manual_status
  8628-8629   _mark_dead
 12202-12218  _marketing_loop
 24768-24786  _maybe_handle_command
 27158-27182  _maybe_hype_clip
 23740-23768  _meme_klassifizieren
 20105-20167  _meme_zusammenschnitt
  4400-4405   _migrate_columns
 25050-25061  _mod_is_exempt
 25064-25069  _mod_warn_first
 25072-25075  _mod_warn_text
 13854-13873  _modlog
 13837-13851  _modlog_schreiben
  1106-1108   _multistream_targets
  3336-3372   _nachschlag_ytdlp
  8265-8266   _nc_create_subprocess_exec
  8269-8270   _nc_create_subprocess_shell
 12525-12542  _news_loop
 13896-13898  _normalize_ingest
  2673-2690   _note_check_duration
  9686-9689   _notify_topic_name
  2877-2883   _offline_ergebnis
  3375-3398   _ohne_url_melden
 18603-18611  _oracle_memories
 18900-18934  _oracle_memorize
 18614-18627  _oracle_persona
 18596-18600  _oracle_recent_text
 14294-14295  _ov_atomic_write
 14285-14287  _ov_bar
 17431-17443  _ov_clip_text
 14290-14291  _ov_oneline
 22275-22304  _overlay_push
 14624-14667  _overlay_render_size
 13965-13969  _overlay_session_reset
 22240-22242  _overlay_src_ok
 14304-14316  _overlay_takt
 17514-17524  _own_invites
 14619-14621  _parse_size
 22780-22860  _parse_ssh_attacks
  7630-7663   _pause_resume_cmd
  2211-2255   _persist_refreshed_cookies
  2114-2146   _pick_checked_pull_proxy
 10926-10941  _pin_auth_value
 11030-11031  _pin_clear_fail
 10994-10997  _pin_global_gesperrt
 10947-10958  _pin_hmac_schluessel
 11000-11007  _pin_locked
 11010-11027  _pin_note_fail
 10961-10982  _pin_ok
 22068-22093  _piper_pick_model
 22153-22218  _piper_say
 13463-13498  _post_json_threaded
 14598-14616  _probe_video_size
  1997-2014   _proc_is_recorder
 11895-11923  _proxy_pool_refresh_loop
  2080-2111   _proxy_report_recording
  9339-9420   _pruef_runde
  9298-9336   _pruefstand_melden
 26368-26379  _pruefung_verworfen
 13113-13115  _prune_stall_dumps
 12272-12444  _public_stats
  2277-2283   _pull_proxy_still
 19170-19196  _push_notify
 11222-11224  _pwa_dir
 11673-11688  _quick_validate_proxy
 13529-13531  _quiet_hours_config
 11187-11220  _rate_guard
  2902-2930   _raumsperre_fragen
 18415-18421  _react_warn
  8167-8206   _reap_proc
 10879-10895  _rebinding_melden
 10030-10097  _rec_auto_abschalten
  9977-10027  _rec_frueh_getrennt
  9842-9922   _rec_kategorie_melden
  9925-9974   _rec_totstreak_fortschreiben
  2713-2735   _record_check_outcome
   831-833    _redact_stream_urls
 11822-11892  _refresh_proxy_pool
  2490-2581   _resolve_via_html
  2933-3129   _resolve_via_webcast_api_v2
  3197-3284   _resolve_via_ytdlp
 24377-24506  _resolve_youtube_ingest
  2466-2487   _resolver_stumm
 13948-13959  _restream_active_sources
 15022-15149  _restream_avatar_feeder_start
 15152-15162  _restream_avatar_feeder_stop
 20255-20393  _restream_chat_guardian
 14122-14194  _restream_chat_push
 14271-14280  _restream_chat_push_async
 27387-27442  _restream_durchreicher
 14732-14857  _restream_html_overlay_start
 14879-14899  _restream_html_overlay_stop
 13907-13930  _restream_overlay_files
 20888-20920  _restream_platform_state
 21088-21123  _restream_resume_after_restart
 14225-14242  _restream_soll_schreiben
 14245-14268  _restream_status_schreiben
 15210-15282  _restream_tts_enqueue_wav
 14560-14592  _restream_tts_feeder
 14557-14558  _restream_tts_fifo_path
 15165-15192  _restream_tts_start
 15194-15208  _restream_tts_stop
 20926-21085  _restream_verify_loop
 23298-23310  _retention_loop
 23292-23295  _retention_scan
  2834-2836   _room_is_abo
  6374-6491   _run_ai_call
 13256-13269  _run_async_from_flask
 22603-22606  _run_priv
 28318-28326  _run_selfcheck_and_exit
 23313-23324  _s3_client
  8655-8725   _safe_send
  5219-5235   _sample_net_throughput
  2779-2809   _schedule_next_check
 23246-23289  _scheduler_loop
  4408-4410   _schema_pk
 13273-13278  _scraper_session
 25078-25117  _screen_full
 12629-12666  _sec_headers
  2450-2452   _select_stream_from_data_section
 28035-28315  _selfcheck
  9698-9732   _send_live_notice
  1433-1437   _should_defer_upload
 23821-23859  _shrink_for_discord
 11227-11239  _sicheres_ziel
 23126-23164  _sicherheits_erinnerung_loop
 27079-27096  _sign_health_check
 27099-27118  _sign_health_loop
  4970-4995   _sitzung_bestimmen
 21370-21380  _sparen_lage
  8282-8293   _spawn
 28749-28779  _spawn_from_flask
 26382-26388  _speicher_maps
 26391-26406  _speicher_pflegen
 19478-19776  _start_chat_listener
 26351-26365  _start_gesperrt
 13236-13253  _start_loop_watchdog
 12471-12520  _stats_loop
 12450-12453  _stats_output_path
 12456-12468  _stats_write
 22105-22119  _stimme_saubern
 22126-22150  _stimme_schon_gesagt
  9279-9295   _storage_cleanup_loop
 27138-27145  _story_for
  3728-3734   _stream_url_expiry
  3736-3741   _stream_url_ttl
 17477-17484  _streamer_persona_get
 23430-23582  _system_backup
 23591-23621  _system_backup_loop
 13073-13091  _task_auf_bot_schleife
 25915-25931  _telegram_befehlsmenue
  8336-8382   _telegram_polling_fehler
  1478-1505   _telegram_ziele
 11625-11664  _test_proxy
 12150-12166  _testpush_resolve_live
 20178-20180  _text_schreiben
  9750-9760   _tg_migriert_laden
  9746-9747   _tg_migriert_pfad
  8631-8652   _tg_sprache_setzen
  9560-9570   _tg_topics_load_into_mem
  9557-9558   _tg_topics_path
  9572-9579   _tg_topics_save
 10898-10908  _token_ok
  9657-9673   _topic_anlegen
  9582-9589   _topic_forget
 13549-13560  _tracking_max_duration
  4705-4719   _tracking_remove_cleanup
  4736-4748   _tracking_resume_cleanup
  1808-1831   _try_attach_file_handler
 22095-22103  _tts_cleanup
 12126-12130  _tunnel_effective
 26803-26823  _tunnel_lage
 26964-27016  _tunnel_wacht_loop
 21594-21647  _twitch_channel_status
 25120-25268  _twitch_chat_loop
 24172-24185  _twitch_clip_versuchen
 24931-25037  _twitch_eventsub_loop
  1598-1633   _upload_queue_abarbeiten
  1456-1476   _upload_queue_add
  1569-1571   _upload_queue_count
  1439-1448   _upload_queue_load
  1636-1658   _upload_queue_nachher
  1429-1431   _upload_queue_path
  1555-1559   _upload_queue_remove
  1450-1454   _upload_queue_save
  1562-1567   _upload_queue_update
 10130-10154  _upload_rest_sichern
  1573-1595   _upload_window_loop
  8140-8147   _uptime_s
 13884-13893  _url_host
  3401-3499   _url_nachschlag
   913-917    _usage_record_claude
 27252-27274  _v37_pause_source
 27216-27226  _v37_restream_restart
 27229-27249  _v37_unpause_source
  8554-8598   _verbindung_verloren
  7104-7135   _viewer_sample_loop
 11034-11037  _wants_html
  8150-8164   _warn_empty_env
 26610-26735  _watchdog_loop
 24652-24660  _wchat_thank_ok
 26931-26961  _werkzeug_wacht_loop
 19238-19276  _whisper_get_model
  8241-8249   _whisper_native_section
 18402-18408  _whisper_pool
 19370-19402  _whisper_segments
 19278-19294  _whisper_stumm
 19297-19367  _whisper_transcribe
 14357-14514  _write_restream_overlay
 14319-14354  _write_restream_overlay_async
 25292-25391  _youtube_api_chat_loop
 21650-21753  _youtube_api_status
 21756-21823  _youtube_channel_status
 25394-25558  _youtube_chat_loop
 24188-24213  _youtube_clip_versuchen
 24512-24525  _youtube_restream_autoconfig
 24528-24552  _youtube_restream_autoconfig_inner
 24619-24647  _youtube_send
 21891-21932  _youtube_set_channel
 24555-24589  _yt_access_token
 24592-24607  _yt_live_chat_id
 24615-24616  _yt_sendrate_cfg
 25271-25286  _yt_timeout
  3176-3177   _ytdlp_detect_available
  3192-3194   _ytdlp_einzeln
  3179-3190   _ytdlp_note_result
 13118-13120  _zombie_child_count
 26441-26454  _zustand_kennzahlen
  8016-8040   about
  4616-4620   add_ai_log_entry
  4533-4536   add_archive_entry
  5252-5254   add_archive_rule
  4998-5069   add_recording
  4680-4697   add_tracking
  6494-6527   ai
  4144-4239   ai_chat
  4338-4348   ai_history_append
  4350-4355   ai_history_clear
  4327-4336   ai_history_load
  4312-4325   ai_rate_limit_check
  6556-6564   aireset
 18767-18786  azrael_chat
 25563-25685  brain_cmd
  3744-3749   build_recording_cmd
  4700-4703   bulk_add_trackings
  7383-7442   bulkadd
  9423-9539   check_all_trackings
  4752-4764   claim_live_transition
 17570-18334  class KickModerator
 15359-17318  class RestreamManager
  4918-4919   class _AufnahmeLockVerloren
  8490-8551   class _KickClusterSuche
 12009-12051  classify_proxy_anonymity
  6602-6801   cleanup
  5542-5548   cleanup_old_recordings
  4943-4950   clear_recording
 24216-24237  clip_moment
  5210-5213   compute_storage_forecast
  7505-7581   cookies_cmd
  7584-7627   cookies_datei_cmd
  4671-4677   count_trackings_for_chat
  4603-4614   decide_preferred_recorder
  4543-4546   delete_archive_entry
  5256-5258   delete_archive_rule
  6031-6178   diag
 25797-25858  einnahmen_cmd
  5204-5207   find_recordings_by_fingerprint
  4564-4580   finish_recording_attempt
  4724-4726   get_all_active_trackings
  4631-4633   get_all_checks
  5071-5074   get_all_recordings
  5153-5155   get_all_tags_with_counts
  5181-5184   get_annotations_for_recording
  4538-4541   get_archive_entry
  5174-5177   get_bookmarked_recordings
  2317-2322   get_cookie_health
  5141-5147   get_event_log
  4587-4601   get_last_recording_attempt
  3502-3544   get_live_status
  5481-5484   get_manual_recordings
  5189-5192   get_or_compute_inspect_sync
  5583-5586   get_outcome_breakdown
  5160-5163   get_priority_poll_interval
  4582-4585   get_recent_recording_attempts
  5076-5079   get_recording_by_id
  5167-5170   get_recording_note
  3915-3944   get_redis
  4660-4663   get_stats
  5536-5540   get_storage_stats
  5276-5278   get_tiktok_status_distribution
  4766-4775   get_tracking_state
  4721-4722   get_trackings_for_group
  5497-5500   get_trash_recordings
 10218-10685  handle_recording_finished
 25907-25912  hilfe_cmd
  4423-4488   init_db
  5248-5250   list_archive_rules
  5816-5854   live
  8728-8758   live_check_worker
  3999-4041   llm_chat
  4076-4108   llm_chat_sync
  4061-4073   llm_list_models
  5100-5133   log_event
  1931-1964   log_recording_failure
  7777-7826   logs_cmd
 27746-28025  main
  6530-6553   on_ai_media
  7903-7929   on_ai_reply
  7984-8013   on_azrael_mention
  8045-8075   on_callback
  9805-9823   on_chat_migration
  7938-7951   on_link_video
 18792-18897  oracle_handle
  7666-7669   pause_tracking
  5596-5601   profile_keyboard
  5769-5813   quelle
  7728-7774   quota
  9202-9276   reaper_loop
  5272-5274   record_tiktok_status
  6569-6599   recstatus
  3946-3954   redis_get_json
  3957-3963   redis_set_json
 25934-25944  report_cmd
 12054-12056  report_proxy_result
  2584-2626   resolve_tiktok_live_stream
  5492-5495   restore_recording
  7672-7675   resume_tracking
  5261-5266   run_archive_rules
 25947-26219  run_bot
 12970-13064  run_flask
  4623-4629   save_tiktok_check
  4922-4941   set_recording_file
  4729-4733   set_tracking_paused
  5487-5490   soft_delete_recording
 25892-25904  spenden_cmd
  9829-9840   split_and_send_video
  5679-5721   start
  4548-4562   start_recording_attempt
  6804-6842   stats
  5426-5479   stop_manual_recording
  7678-7725   stoprec
  7028-7036   summary_cmd
  7829-7900   sysres
  6180-6324   teststream
  5723-5764   tiktok
  7445-7502   topusers
  5891-5948   track
  5856-5888   track_exact
  5962-6029   tracklist
  5310-5424   trigger_manual_recording
  4854-4889   try_acquire_recording_lock
  5503-5505   universal_search
 25861-25889  unpause_cmd
  5950-5960   untrack
 25688-25794  update_cmd
  5199-5202   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
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
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, host_ist_lokal, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, class KeinDesktop, configure, desktop_pruefen, hole_gastcookies, schreibe, uebernehmen, zusammenfuehren
cookies.py             configure, gesundheit, hat_login, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
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
discordziele.py        clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, loeschbar, umzugsmarke, umzugsmarke_lesen
donations.py           configure, fmt_eur, kurse_aus_env, parse_number, summe_eur, to_eur, unknown_count, zeile_eur
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       bekannt, class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
encodeschlange.py      lage, last_frei, parallel, platz, platz_sync
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
forkriegel.py          class Vortritt
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
heapzaum.py            arenen_wunsch, deckeln, lage, rss_mb, takt_min, zurueckgeben
herkunft.py            entscheiden
highlights.py          check, new_state, observe, score, zustand
httpsitzung.py         schliessen, sitzung, teilen
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, state_gueltig, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              azrael_lage, azrael_wahl, backend, gesamtzeit, llm_zeiten, lokal_installiert, lokal_stand, lokal_zuerst, lokales_modell, normal, provider, vorrang, wartezeit, weg_zaehlen, zeitlimit
lagebild.py            bauen, dienst_quelle, dienste, dienste_lesen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
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
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler, lage, teilen
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
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
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
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
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             class BestandUnbekannt, cleanup, forecast, notfall_raeumen, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, text, zuruecksetzen
textmore.py            configure_banned_cap, pre_nachrichten, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
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
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
werkzeugpfad.py        alter_tage, befund, lage, nachahmen_aus, pruefen, voranstellen
whispercfg.py          bedarf_mb, benutzt, entladen_wenn_leer, frei_mb, gebrauch, geladen, leerlauf_s, name, rss_hinweis, verfuegbar, waehle, wechsel_pruefen
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
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
