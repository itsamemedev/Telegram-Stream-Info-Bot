# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (153)

```
 10454  GET              /                                                dashboard
 14143  GET              /api/abo/status                                  api_abo_status
 10527  GET              /api/active-recordings                           api_active_recordings
 14214  GET              /api/activity-pulse                              api_activity_pulse
 14021  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 20779  GET/POST         /api/audio/config                                api_audio_config
 20809  POST             /api/audio/testtone                              api_audio_testtone
 14087  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14111  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14115  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11981  GET              /api/automation/status                           api_automation_status
 12003  POST             /api/automation/toggle                           api_automation_toggle
 13018  GET              /api/azrael/agents                               api_azrael_agents
 11873  POST             /api/azrael/ask                                  api_azrael_ask
 20977  GET/POST         /api/azrael/context                              api_azrael_context
 12723  GET              /api/azrael/core                                 api_azrael_core
 21120  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21110  GET              /api/azrael/live_status                          api_azrael_live_status
 21128  POST             /api/azrael/live_test                            api_azrael_live_test
 13027  GET              /api/azrael/memories                             api_azrael_memories
 21176  POST             /api/azrael/persona                              api_azrael_persona_set
 21167  GET              /api/azrael/personas                             api_azrael_personas
 21204  GET              /api/azrael/piper_status                         api_azrael_piper_status
 20950  POST             /api/azrael/react                                api_azrael_react
 20986  GET              /api/azrael/reaction                             api_azrael_reaction
 21147  GET              /api/azrael/reactions                            api_azrael_reactions
 21197  GET              /api/azrael/transcript                           api_azrael_transcript
 21082  POST             /api/azrael/tts_test                             api_azrael_tts_test
 21053  GET              /api/azrael/voices                               api_azrael_voices
 21221  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10826  GET              /api/backoff-watch                               api_backoff_watch
 13502  POST             /api/backup/run                                  api_backup_run
 13468  GET              /api/backup/status                               api_backup_status
 13457  POST             /api/backup/system                               api_backup_system
 14053  GET              /api/bandwidth/live                              api_bandwidth_live
 14006  GET              /api/bookmarks                                   api_bookmarks_list
 11089  GET              /api/brain                                       api_brain
 11026  GET              /api/brain/alarms                                api_brain_alarms
 11011  GET              /api/brain/creator                               api_brain_creator
 10988  GET              /api/brain/graph                                 api_brain_graph
 11049  GET              /api/brain/growth                                api_brain_growth
 10004  GET              /api/brain/health                                api_brain_health
 21665  GET              /api/channel/categories                          api_channel_categories
 21671  POST             /api/channel/set                                 api_channel_set
 21518  GET              /api/channels/status                             api_channels_status
 20423  POST             /api/chat/send                                   api_chat_send
 13222  GET              /api/chat/send_status                            api_chat_send_status
 10508  GET              /api/checks                                      api_checks
 21014  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20997  GET              /api/clips                                       api_clips
 21035  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20701  GET              /api/cohost                                      api_cohost
 20713  POST             /api/cohost/config                               api_cohost_config
 14522  GET              /api/community/stats                             api_community_stats
 22305  GET              /api/data/export                                 api_data_export
 20627  GET              /api/debug/threads                               api_debug_threads
 23132  GET              /api/defense/attacks                             api_defense_attacks
 23099  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23117  GET              /api/defense/fail2ban                            api_defense_fail2ban
 22823  GET              /api/defense/overview                            api_defense_overview
 13564  POST             /api/discord/announce                            api_discord_announce
 13292  GET              /api/discord/clips_week                          api_discord_clips_week
 13508  GET              /api/discord/community                           api_discord_community
 13250  GET              /api/discord/invite                              api_discord_invite
 12824  GET              /api/discord/overview                            api_discord_overview
 12910  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14035  GET              /api/events                                      api_events
 13339  GET              /api/events/stream                               api_events_stream
 14048  GET              /api/forecast/storage                            api_forecast_storage
 12019  GET              /api/freeai/status                               api_freeai_status
 12766  GET              /api/health                                      api_health
 14066  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14062  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20750  GET              /api/highlights                                  api_highlights
 20762  POST             /api/highlights/config                           api_highlights_config
 20858  POST             /api/kickmod/config                              api_kickmod_config
 20903  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 20917  GET              /api/kickmod/learned                             api_kickmod_learned
 20944  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 20924  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21264  POST             /api/kickmod/say                                 api_kickmod_say
 21240  POST             /api/kickmod/start                               api_kickmod_start
 20829  GET              /api/kickmod/status                              api_kickmod_status
 21251  POST             /api/kickmod/stop                                api_kickmod_stop
 10388  POST             /api/login                                       dashboard_login_submit
 14507  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14476  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13187  GET              /api/notify/status                               api_notify_status
 13198  POST             /api/notify/test                                 api_notify_test
 10612  GET              /api/outcomes                                    api_outcomes
 22142  POST             /api/overlay/config                              api_overlay_config
 22129  POST             /api/overlay/event                               api_overlay_event
 22034  GET              /api/overlay/state                               api_overlay_state
 10645  GET              /api/profile/<username>                          api_profile
 14232  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14074  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14197  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14174  GET              /api/proxy/trend                                 api_proxy_trend
 12474  GET              /api/public/stats                                api_public_stats
 10488  GET              /api/pulse                                       api_pulse
 13642  GET              /api/recording-attempts                          api_recording_attempts
 20358  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20336  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20377  POST             /api/restream/<int:rid>/start                    api_restream_start
 20648  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 21996  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20312  POST             /api/restream/create                             api_restream_create
 12599  GET              /api/restream/deck                               api_restream_deck
 11955  GET              /api/restream/health                             api_restream_health
 22018  POST             /api/restream/layout                             api_restream_layout
 20285  GET              /api/restream/list                               api_restream_list
 11924  POST             /api/restream/report                             api_restream_report
 20661  POST             /api/restream/start_all                          api_restream_start_all
 20687  POST             /api/restream/stop_all                           api_restream_stop_all
 12130  GET              /api/restream/testpush                           api_testpush_status
 12155  POST             /api/restream/testpush                           api_testpush_run
 14607  GET              /api/restream/verify                             api_restream_verify
 13270  GET              /api/retention/preview                           api_retention_preview
 13279  POST             /api/retention/run                               api_retention_run
 13991  GET              /api/search                                      api_search
 22870  GET              /api/selftest                                    api_selftest
 20394  GET              /api/shield/stats                                api_shield_stats
 10549  GET              /api/storage                                     api_storage
 10556  POST             /api/storage/cleanup                             api_storage_cleanup
 14128  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11894  GET              /api/stream/timeline                             api_stream_timeline
 12898  GET              /api/stream/transcript                           api_stream_transcript
 10580  GET              /api/summary/preview                             api_summary_preview
 13707  GET              /api/system                                      api_system
 14555  GET              /api/system/check_timing                         api_check_timing
 14670  GET              /api/system/config_drift                         api_config_drift
 12934  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13045  GET              /api/system/preflight                            api_system_preflight
 13171  GET              /api/system/preflight_history                    api_system_preflight_history
 13404  GET              /api/system/resilience                           api_system_resilience
 14026  GET              /api/tags                                        api_tags_list
 10522  GET              /api/top                                         api_top
 10881  GET              /api/trend-7d                                    api_trend_7d
 21067  GET              /api/tts/<fn>                                    api_tts_file
 22170  GET              /api/upload_window                               api_upload_window
 10626  GET              /api/userstats                                   api_userstats
 12522  GET              /api/version                                     api_version
 13680  GET              /archive/<int:eid>/download                      archive_download
 13737  GET              /download/<int:recording_id>                     download
 13620  GET              /health                                          health
 20596  GET              /healthz                                         healthz
 10379  GET              /login                                           dashboard_login_page
 10409  GET              /logout                                          dashboard_logout
 10416  GET              /manifest.webmanifest                            pwa_manifest
 12962  GET              /metrics                                         api_prometheus_metrics
 21979  GET              /overlay                                         overlay_page
 10440  GET              /pwa-icon-<variant>.png                          pwa_icon
 10426  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (206)

```
   176  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   146  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   148  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   133  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    73  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
    95  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   116  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    63  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   163  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    27  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    57  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    46  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   204  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    70  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   203  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   225  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    84  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   130  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    69  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   109  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   159  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
    61  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    86  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
    96  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    35  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    53  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    83  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    49  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    60  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   125  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   120  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   111  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    36  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    75  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   815  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   897  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   925  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   936  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   802  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   864  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   851  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   832  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   477  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   472  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   520  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   403  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   494  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   457  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   430  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   704  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   574  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   663  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   569  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   282  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   747  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   370  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   625  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   780  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   765  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   326  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   564  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   550  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   533  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   590  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   683  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   579  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   109  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   200  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   195  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   255  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   109  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   256  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    71  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   281  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   213  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   237  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   168  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   133  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   193  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    39  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   219  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   434  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   463  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   383  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   492  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   369  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   244  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   289  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   300  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   146  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   258  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   116  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   350  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   405  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   106  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    58  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    82  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    36  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   114  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   135  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   147  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    72  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
    96  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    50  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   182  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
```

## Discord-Slash-Commands (45)

```
 23596  /ai                     
 24055  /ask                    
 23687  /assign_role            
 23733  /ban                    
 24387  /botstats               
 24311  /clearwarns             
 24351  /clip                   
 24336  /clipoftheweek          
 24178  /clips                  
 23648  /create_category        
 23617  /create_channel         
 23676  /create_group           
 23659  /create_role            
 23633  /create_voice           
 23969  /daily                  
 24085  /event                  
 24128  /events                 
 24224  /follow                 
 24208  /help                   
 23722  /kick                   
 23951  /leaderboard            
 24164  /livenow                
 24194  /post_test              
 24025  /profile                
 23757  /purge                  
 23937  /rank                   
 24151  /recstatus              
 23698  /remove_role            
 23610  /restream_status        
 23709  /set_channel_perms      
 23902  /setup_community        
 23920  /setup_targets          
 24250  /stats                  
 23522  /status                 
 24546  /streaminfo             
 24443  /sys_report             
 24419  /sys_unpause            
 23744  /timeout                
 24322  /topstreamers           
 23552  /track                  
 23536  /tracklist              
 24239  /unfollow               
 23585  /untrack                
 24272  /warn                   
 24296  /warnings               
```

## Discord-Events (4)

```
 25030  on_member_join
 24992  on_message
 24633  on_raw_reaction_add
 25065  on_ready
```

## Top-Level-Symbole in bot.py (510 Funktionen, 2 Klassen)

```
  2495-2496   _abo_key
  2516-2534   _abo_probe_dump
 22412-22422  _active_recorder_sync
 17574-17581  _ad_allowlist
 18701-18707  _agent_for
 22424-22442  _ai_calls_total_sync
 18710-18726  _ai_telemetry
 19208-19226  _alert
 25181-25231  _alert_monitor_loop
 25612-25674  _announce_loop
  3437-3440   _anthropic_key
  3447-3449   _anthropic_model
 10132-10135  _arg_int
  2487-2492   _as_dict
 15351-15356  _audio_cfg
 19362-19384  _audio_tap_cmd
 10300-10311  _auth_cookie
 10267-10296  _auth_guard
  1643-1648   _auto_on
 20261-20279  _auto_restream_loop
 26733-26748  _azrael_broadcast_reply
 26633-26655  _azrael_chat_reply
 26616-26630  _azrael_chat_should_reply
 26661-26663  _azrael_gate_cfg
 18731-18745  _azrael_live_state
 21882-21896  _azrael_overlay_state
 19091-19145  _azrael_proactive_loop
 18550-18606  _azrael_reaction_to_chats
 26666-26673  _azrael_reply_all_chats
 26603-26613  _azrael_self_names
 26701-26730  _azrael_send_to
 18748-18769  _azrael_system
 25350-25353  _backup_active
 25431-25444  _backup_loop
 17462-17463  _badwords_path
 25143-25152  _brain_growth_loop
 10957-10984  _brain_growth_snapshot
  2423-2443   _brain_hint_delay
 10949-10951  _brain_history_for
  6516-6544   _brain_notify
 10926-10947  _brain_record
 10953-10955  _brain_stream_recent
 13318-13335  _browser_push
  6560-6647   _build_daily_summary
  2926-3106   _build_native_cmd
 15712-15899  _build_restream_cmd
  3150-3183   _build_ytdlp_cmd
 22364-22371  _cached_probe
  5338-5365   _can_stop_tracking
  1823-1845   _capture_set_cookies
 14291-14294  _cfg_get
 14297-14299  _cfg_set
 21626-21661  _channel_set_all
 14949-14952  _chat_connected
 14955-14971  _chat_disconnected
  8612-8623   _chat_is_forum
 14991-14993  _chat_sanitize
 14995-15004  _chat_src_ok
 14934-14946  _chat_stat
 14974-14977  _chat_stats_snapshot
  3712-3723   _check_ai_alive_sync
  3726-3738   _check_ai_models_sync
 22373-22386  _check_redis_alive_sync
 22388-22408  _check_redis_version_sync
 11556-11599  _classify_pool_anonymity
 11602-11619  _classify_pool_anonymity_bg
   801-805    _claude_chat_sync_metered
 10161-10168  _client_ip
 25706-25733  _clip_prune
 25736-25746  _clip_recfile_for
 26262-26268  _clip_should_velocity
 25787-25869  _clip_to_discord
  3610-3619   _close_ai_session
 26777-26792  _cohost_broadcast
 26759-26763  _cohost_cfg
 26818-26830  _cohost_fire_highlight
 26766-26774  _cohost_gate
 26795-26815  _cohost_highlight
 25918-25952  _community_events_loop
 10780-10782  _conv_messages
  6924-6967   _cookie_alarm_loop
  1895-1899   _cookie_autorefresh_info
  1800-1804   _cookie_header
 13368-13400  _cpu_load_snapshot
  3920-3932   _create_index_safe
 22625-22731  _crowdsec_status
 22591-22622  _crowdsec_via_lapi
 22456-22474  _cscli_bin
 22480-22493  _cscli_path
  6814-6839   _daily_summary_loop
 22511-22528  _darf_journal_lesen
 25155-25178  _db_maintenance_loop
  6783-6811   _db_vacuum_loop
 17597-17621  _detect_foreign_ad
  1381-1392   _diag_path_owner
 18997-19041  _director_finalize
 19808-19815  _director_for
 18946-18994  _director_mark
 26156-26191  _disc_automod_check
 26129-26135  _disc_state_get
 26138-26145  _disc_state_set
 23174-23187  _discord_guild_filesize_bytes
 23373-23382  _discord_invite
 26090-26126  _discord_live_thread
 19148-19160  _discord_notify
 23274-23299  _discord_ops_alert
 25988-26086  _discord_post_user
 23438-25140  _discord_run_once
 23312-23370  _discord_start
 25677-25683  _discord_stop
 23195-23197  _discord_upload_limit_label
 23190-23192  _discord_upload_limit_mb
  6842-6919   _disk_alarm_loop
 28184-28233  _disk_autoclean
 28236-28249  _disk_guard_loop
 28176-28181  _disk_pct
 15308-15310  _drawtext_chain
 13834-13836  _dump_all_threads
 11481-11545  _enrich_proxies_with_geo
  2040-2084   _ensure_cookie_file_netscape
 23385-23435  _ensure_discord_invite
 25883-25915  _ensure_error_channel
  8671-8674   _ensure_notify_topic
 11726-11763  _ensure_proxy_ready
  8625-8652   _ensure_topic
   658-660    _env_int
   663-665    _env_int_range
 25955-25985  _error_channel_loop
 19192-19205  _event_webhook
 14757-14770  _evolution_loop
  5958-5992   _extract_file_payload
  2172-2174   _extract_urls_from_streamurl_node
 22496-22503  _f2b_sudo_hint
 19228-19230  _faster_whisper_available
 17486-17498  _fetch_ldnoobw_de
 11370-11388  _fetch_proxy_list
 19642-19670  _fetch_tiktok_room_id
   734-737    _ff_cmd
 15471-15476  _find_chromium
  3143-3147   _find_external_recorder
  2177-2179   _find_stream_urls
 14342-14367  _fire_webhooks
  7703-7712   _fork_safe
   816-825    _freeai_chat_sync_metered
 22546-22588  _geo_lookup_ips
  3599-3608   _get_ai_session
  7537-7577   _get_live_info
  2713-2720   _get_resolve_semaphore
  7967-8333   _handle_single_tracking
 28028-28030  _hb
 28033-28050  _hb_while
 15009-15011  _highlight_cfg
 15014-15043  _highlight_observe
 15479-15497  _htmlov_screenshot_cmd
 19386-19396  _httpx_proxy
 14375-14387  _in_quiet_hours
 29063-29094  _install_fast_eventloop
 10027-10081  _install_fast_json
 13839-13855  _install_faulthandler
 20504-20513  _intel_ensure_schema
 20551-20586  _intel_index_loop
 20525-20535  _intel_index_one
 20516-20522  _intel_semantic
  5327-5336   _is_authorized
  7868-7874   _is_dead
  2162-2164   _is_hevc
 22531-22537  _is_private_ip
  1545-1552   _is_process_running
  6546-6557   _is_quiet_hours
  1182-1191   _is_upload_window
 10116-10129  _json_error_handler
  6769-6770   _kick_broadcaster_id
 12056-12075  _kick_channel_live
  6681-6723   _kick_follower_count
  6665-6668   _kick_slug
 12549-12580  _kick_user_token
  3969-3972   _kind_from_filename
 14404-14409  _latest_popularity
 17508-17514  _learned_load
 17505-17506  _learned_path
 17516-17524  _learned_save
 20023-20056  _live_react_loop
 19819-20012  _live_react_worker
 18609-18620  _live_transcript_push
 20014-20021  _live_users
 19044-19088  _living_title_loop
 17465-17473  _load_banned_words_file
  1721-1794   _load_cookies_dict
 25356-25428  _local_backup_scan
 10098-10112  _log_5xx
 15907-15919  _looks_like_codec_err
 15902-15904  _looks_like_source_expired
  7784-7814   _loop_fehler
 13859-13868  _loop_heartbeat
 27998-28025  _loop_lag_monitor
 13871-13939  _loop_watchdog_thread
 18489-18503  _loyalty_add
 18480-18486  _loyalty_get
 18506-18514  _loyalty_top
 14541-14543  _manual_donations_total
  7876-7877   _mark_dead
 12227-12243  _marketing_loop
 26680-26698  _maybe_handle_command
 28335-28359  _maybe_hype_clip
  3887-3910   _migrate_columns
 26957-26968  _mod_is_exempt
 26971-26976  _mod_warn_first
 26979-26982  _mod_warn_text
 14797-14805  _modlog
   935-937    _multistream_targets
  7715-7716   _nc_create_subprocess_exec
  7719-7720   _nc_create_subprocess_shell
 12479-12496  _news_loop
 14835-14837  _normalize_ingest
  2354-2371   _note_check_duration
  8665-8668   _notify_topic_name
 18635-18643  _oracle_memories
 18901-18935  _oracle_memorize
 18646-18659  _oracle_persona
 18628-18632  _oracle_recent_text
 15134-15142  _ov_atomic_write
 15122-15128  _ov_bar
 17421-17433  _ov_clip_text
 15131-15132  _ov_oneline
 21946-21975  _overlay_push
 15425-15468  _overlay_render_size
 14896-14900  _overlay_session_reset
 21898-21901  _overlay_src_ok
 17584-17594  _own_invites
 15420-15422  _parse_size
 22739-22819  _parse_ssh_attacks
  7139-7172   _pause_resume_cmd
  1849-1893   _persist_refreshed_cookies
  1687-1719   _pick_checked_pull_proxy
 10197-10210  _pin_auth_value
 10256-10257  _pin_clear_fail
 10236-10239  _pin_locked
 10242-10253  _pin_note_fail
 10213-10233  _pin_ok
 21788-21790  _piper_available
 21753-21775  _piper_list_voices
 21795-21820  _piper_pick_model
 21832-21879  _piper_say
 21746-21750  _piper_voice_roots
 14304-14339  _post_json_threaded
 15399-15417  _probe_video_size
  1573-1590   _proc_is_recorder
 11468-11479  _proxy_geo_cache_put
 11695-11723  _proxy_pool_refresh_loop
  1653-1684   _proxy_report_recording
 13824-13826  _prune_stall_dumps
 12297-12418  _public_stats
 19163-19189  _push_notify
 10358-10360  _pwa_dir
 11439-11454  _quick_validate_proxy
 14370-14372  _quiet_hours_config
 10323-10356  _rate_guard
 18454-18460  _react_warn
  7623-7662   _reap_proc
  2394-2416   _record_check_outcome
   729-731    _redact_stream_urls
 11622-11692  _refresh_proxy_pool
 21778-21784  _resolve_piper_model
  2188-2278   _resolve_via_html
  2536-2690   _resolve_via_webcast_api_v2
  2753-2815   _resolve_via_ytdlp
 26307-26436  _resolve_youtube_ingest
 20095-20102  _restream_active_platforms
 14881-14892  _restream_active_sources
 19673-19772  _restream_chat_guardian
 15046-15118  _restream_chat_push
 14808-14820  _restream_enabled
 15500-15587  _restream_html_overlay_start
 15590-15603  _restream_html_overlay_stop
  1130-1132   _restream_layout_mode
 14846-14869  _restream_overlay_files
 20060-20092  _restream_platform_state
 20223-20258  _restream_resume_after_restart
 15651-15709  _restream_tts_enqueue_wav
 15361-15393  _restream_tts_feeder
 15358-15359  _restream_tts_fifo_path
 15606-15633  _restream_tts_start
 15635-15649  _restream_tts_stop
 20105-20220  _restream_verify_loop
 25321-25333  _retention_loop
 25280-25318  _retention_scan
  2498-2500   _room_is_abo
  5996-6113   _run_ai_call
 13962-13975  _run_async_from_flask
 22540-22543  _run_priv
 29051-29059  _run_selfcheck_and_exit
 25336-25347  _s3_client
  7903-7954   _safe_send
  4591-4607   _sample_net_throughput
 17475-17483  _save_banned_words_file
  2446-2473   _schedule_next_check
 25234-25277  _scheduler_loop
  3913-3917   _schema_pk
 13979-13984  _scraper_session
 26985-27024  _screen_full
 12782-12819  _sec_headers
  2167-2169   _select_stream_from_data_section
 28864-29048  _selfcheck
  8677-8711   _send_live_notice
  1205-1209   _should_defer_upload
 25749-25784  _shrink_for_discord
 10363-10375  _sicheres_ziel
 28256-28273  _sign_health_check
 28276-28295  _sign_health_loop
  7732-7743   _spawn
  7746-7776   _spawn_from_flask
 22863-22866  _st_befund
 19398-19639  _start_chat_listener
 13942-13959  _start_loop_watchdog
 12442-12470  _stats_loop
 12421-12424  _stats_output_path
 12427-12439  _stats_write
  8405-8421   _storage_cleanup_loop
 28315-28322  _story_for
  3205-3211   _stream_url_expiry
  3220-3226   _stream_url_is_fresh
  3213-3218   _stream_url_ttl
 17548-17555  _streamer_persona_get
 17530-17536  _streamer_personas_load
 17527-17528  _streamer_personas_path
 17538-17546  _streamer_personas_save
 15313-15317  _studio_chain
 25453-25575  _system_backup
 25578-25608  _system_backup_loop
 11391-11430  _test_proxy
 12097-12106  _testpush_cfg
 12109-12126  _testpush_exec
 12078-12094  _testpush_resolve_live
  7879-7900   _tg_sprache_setzen
  8584-8594   _tg_topics_load_into_mem
  8581-8582   _tg_topics_path
  8596-8603   _tg_topics_save
 10171-10179  _token_ok
  8606-8610   _topic_forget
 14390-14401  _tracking_max_duration
  4178-4192   _tracking_remove_cleanup
  4209-4221   _tracking_resume_cleanup
  1439-1462   _try_attach_file_handler
 21822-21830  _tts_cleanup
 12034-12038  _tunnel_effective
 21285-21338  _twitch_channel_status
 27027-27170  _twitch_chat_loop
 26841-26944  _twitch_eventsub_loop
  1228-1241   _upload_queue_add
  1252-1254   _upload_queue_count
  1211-1220   _upload_queue_load
  1201-1203   _upload_queue_path
  1243-1250   _upload_queue_remove
  1222-1226   _upload_queue_save
  1256-1297   _upload_window_loop
  7596-7603   _uptime_s
 14823-14832  _url_host
   709-726    _url_ohne_zugang
   794-798    _usage_record_claude
  7817-7861   _verbindung_verloren
  6726-6757   _viewer_sample_loop
  6773-6780   _viewer_stats
 10260-10263  _wants_html
  7606-7620   _warn_empty_env
 28071-28166  _watchdog_loop
 26582-26590  _wchat_thank_ok
 19232-19262  _whisper_get_model
  7693-7700   _whisper_native_section
 18441-18447  _whisper_pool
 19331-19360  _whisper_segments
 19264-19328  _whisper_transcribe
 15144-15306  _write_restream_overlay
 27198-27277  _youtube_api_chat_loop
 21341-21444  _youtube_api_status
 21447-21514  _youtube_channel_status
 27280-27440  _youtube_chat_loop
 26442-26455  _youtube_restream_autoconfig
 26458-26482  _youtube_restream_autoconfig_inner
 26549-26577  _youtube_send
 21582-21623  _youtube_set_channel
 26485-26519  _yt_access_token
 26522-26537  _yt_live_chat_id
 27191-27195  _yt_oauth_configured
 26545-26546  _yt_sendrate_cfg
 27173-27188  _yt_timeout
  2737-2738   _ytdlp_detect_available
  2740-2751   _ytdlp_note_result
 13829-13831  _zombie_child_count
  7473-7497   about
  4088-4092   add_ai_log_entry
  4005-4008   add_archive_entry
  4704-4719   add_archive_rule
  4380-4414   add_recording
  4153-4170   add_tracking
  6116-6149   ai
  3752-3791   ai_chat
  3825-3835   ai_history_append
  3837-3842   ai_history_clear
  3814-3823   ai_history_load
  3799-3812   ai_rate_limit_check
  6178-6186   aireset
 18772-18791  azrael_chat
 27445-27567  brain_cmd
  3229-3413   build_recording_cmd
  4173-4176   bulk_add_trackings
  6970-7029   bulkadd
  8424-8564   check_all_trackings
  4225-4237   claim_live_transition
 17624-18379  class KickModerator
 15922-17308  class RestreamManager
 11808-11850  classify_proxy_anonymity
  6224-6422   cleanup
  5187-5228   cleanup_old_recordings
  4371-4378   clear_recording
 26194-26259  clip_moment
  4535-4584   compute_storage_forecast
  7092-7136   cookies_cmd
  4144-4150   count_trackings_for_chat
  4075-4086   decide_preferred_recorder
  4015-4018   delete_archive_entry
  4721-4729   delete_archive_rule
  5653-5800   diag
 27679-27740  einnahmen_cmd
  4529-4532   find_recordings_by_fingerprint
  4036-4052   finish_recording_attempt
  4197-4199   get_all_active_trackings
  4103-4106   get_all_checks
  4416-4419   get_all_recordings
  4478-4480   get_all_tags_with_counts
  4506-4509   get_annotations_for_recording
  4010-4013   get_archive_entry
  4499-4502   get_bookmarked_recordings
  1916-2033   get_cookie_health
  4466-4472   get_event_log
  4059-4073   get_last_recording_attempt
  2818-2923   get_live_status
  4987-4990   get_manual_recordings
  4514-4517   get_or_compute_inspect_sync
  5263-5307   get_outcome_breakdown
  4485-4488   get_priority_poll_interval
  4682-4691   get_profile_snapshots
  4054-4057   get_recent_recording_attempts
  4421-4424   get_recording_by_id
  4492-4495   get_recording_note
  3547-3570   get_redis
  4133-4136   get_stats
  5154-5185   get_storage_stats
  4822-4824   get_tiktok_status_distribution
  4239-4248   get_tracking_state
  4194-4195   get_trackings_for_group
  5003-5006   get_trash_recordings
  9332-9995   handle_recording_finished
  3935-3960   init_db
  5077-5131   inspect_stream_url
 21941-21943  is_revenue_platform
  4694-4702   list_archive_rules
  5457-5495   live
  7957-7965   live_check_worker
  3622-3656   llm_chat
  3679-3707   llm_chat_sync
  3664-3676   llm_list_models
  4432-4458   log_event
  1507-1540   log_recording_failure
  7286-7335   logs_cmd
 28363-28854  main
  6152-6175   on_ai_media
  7412-7438   on_ai_reply
  7441-7470   on_azrael_mention
  7502-7532   on_callback
 18794-18898  oracle_handle
  7175-7178   pause_tracking
  5317-5322   profile_keyboard
  7237-7283   quota
  8335-8402   reaper_loop
  4818-4820   record_tiktok_status
  6191-6221   recstatus
  3572-3580   redis_get_json
  3582-3588   redis_set_json
 27743-27753  report_cmd
 11853-11855  report_proxy_result
  2281-2308   resolve_tiktok_live_stream
  4998-5001   restore_recording
  7181-7184   resume_tracking
  4732-4812   run_archive_rules
 27756-27978  run_bot
 13751-13798  run_flask
  4610-4655   sample_bandwidth_for_active
  4661-4680   save_profile_snapshot
  4095-4101   save_tiktok_check
  4363-4369   set_recording_file
  4202-4206   set_tracking_paused
  4993-4996   soft_delete_recording
  8717-9330   split_and_send_video
  5370-5412   start
  4020-4034   start_recording_attempt
  6425-6463   stats
  4968-4985   stop_manual_recording
  7187-7234   stoprec
  6650-6658   summary_cmd
  7338-7409   sysres
  5802-5946   teststream
  5414-5455   tiktok
  7032-7089   topusers
  5532-5589   track
  5497-5529   track_exact
  5603-5651   tracklist
  4834-4966   trigger_manual_recording
  4324-4361   try_acquire_recording_lock
  5009-5068   universal_search
  5591-5601   untrack
 27570-27676  update_cmd
  4524-4527   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, url_host
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
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
